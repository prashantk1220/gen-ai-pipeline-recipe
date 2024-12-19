from dotenv import load_dotenv
from haystack.document_stores.types import DuplicatePolicy
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack import Document

load_dotenv()


class DocumentsStore:

    def __init__(self):
        self.document_store = PgvectorDocumentStore(
            language="english",
            embedding_dimension=768,
            vector_function="cosine_similarity",
            recreate_table=True,
            search_strategy="hnsw",
        )


    def load_recipes_to_store(self, recipes: list[dict]):
        """
        Write recipes to document store
        """
        documents = []
        for recipe in recipes:
            document = Document(
                content=f"{recipe['title']}\n\nInstructions:\n{recipe['instructions']}",
                meta={"ingredients": recipe["ingredients"], "title": recipe["title"]},
            )
            documents.append(document)

        self.document_store.write_documents(documents=documents, policy=DuplicatePolicy.SKIP)

        return self.document_store.count_documents()