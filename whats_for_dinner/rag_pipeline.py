from typing import Optional
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from haystack_integrations.components.retrievers.pgvector import (
    PgvectorKeywordRetriever,
)
from haystack.components.generators import OpenAIGenerator

from whats_for_dinner.custom_components import ExtractFoodItemsFromImage

load_dotenv()


class RagPipeline:
    """
    This class initailises the haystack pipeline and provides methods to execute query
    """

    def __init__(self, document_store: PgvectorDocumentStore):
        self.prompt_template = """
            Given these documents, provide a recipe title and instructions with mentioned ingredients.
            \nDocuments:
            {% for doc in documents %}
                {{ doc.content }}
            {% endfor %}
        
            \nIngredients: {{ingredients}}
            \nAnswer:
            """
        self.pipeline = self.create_pipeline(document_store)
        self.image_pipeline = self.create_image_pipeline(document_store)


    def create_pipeline(self, document_store: PgvectorDocumentStore):
        """
        initialises a pipeline for ingredients text retriever
        """
        retriever = PgvectorKeywordRetriever(document_store=document_store)
        rag_pipeline = Pipeline()
        rag_pipeline.add_component(name="retriever", instance=retriever)
        rag_pipeline.add_component(
            instance=PromptBuilder(template=self.prompt_template), name="prompt_builder"
        )
        rag_pipeline.add_component(instance=OpenAIGenerator(model="gpt-4o"), name="llm")

        rag_pipeline.connect("retriever", "prompt_builder.documents")
        rag_pipeline.connect("prompt_builder", "llm")

        return rag_pipeline

    def create_image_pipeline(self, document_store: PgvectorDocumentStore):
        """
        initialises a pipeline for image ingredients retriever
        """
        extract_image_component = ExtractFoodItemsFromImage()
        rag_pipeline_with_image = self.create_pipeline(document_store)
        rag_pipeline_with_image.add_component(instance=extract_image_component, name="food_items_from_image")
        rag_pipeline_with_image.connect("food_items_from_image.answer", "prompt_builder.ingredients")
        rag_pipeline_with_image.connect("food_items_from_image.answer", "retriever.query")

        return rag_pipeline_with_image


    def query_recipe(self, ingredients: Optional[str]=None, image_path: Optional[str]=None):
        """
        Queries the pipline with the provided ingredients or image_path
        """
        if not ingredients and not image_path:
            return None
        if image_path:
            result = self.image_pipeline.run(
                {
                    "food_items_from_image": {"image_path": image_path},
                }
            )
        else:
            result = self.pipeline.run(
                {
                    "retriever": {"query": ingredients},
                    "prompt_builder": {"ingredients": ingredients},
                }
            )
        return result["llm"]["replies"]