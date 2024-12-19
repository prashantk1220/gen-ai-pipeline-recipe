import pytest
from unittest import mock
from whats_for_dinner.rag_pipeline import RagPipeline
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore



@pytest.fixture
def mock_document_store():
    # Mocking PgvectorDocumentStore
    return mock.MagicMock(PgvectorDocumentStore)


@pytest.fixture
def mock_rag_pipeline(mock_document_store):
    # Mock the components used in the RagPipeline
    pipeline = RagPipeline(mock_document_store)

    # Mocking the internal pipeline components
    pipeline.pipeline.run = mock.MagicMock(return_value={"llm": {"replies": ["Recipe based on ingredients"]}})
    pipeline.image_pipeline.run = mock.MagicMock(return_value={"llm": {"replies": ["Recipe based on image"]}})

    return pipeline


def test_query_recipe_with_ingredients(mock_rag_pipeline):
    ingredients = "tomato, cheese, pasta"

    # Call the query_recipe method
    result = mock_rag_pipeline.query_recipe(ingredients=ingredients)

    # Verify the result
    assert result == ["Recipe based on ingredients"]

    # Ensure that the pipeline's run method was called with the expected arguments
    mock_rag_pipeline.pipeline.run.assert_called_with({
        "retriever": {"query": ingredients},
        "prompt_builder": {"ingredients": ingredients},
    })


def test_query_recipe_with_image(mock_rag_pipeline):
    image_path = "path/to/food_image.jpg"

    # Call the query_recipe method
    result = mock_rag_pipeline.query_recipe(image_path=image_path)

    # Verify the result
    assert result == ["Recipe based on image"]

    # Ensure that the image pipeline's run method was called with the expected arguments
    mock_rag_pipeline.image_pipeline.run.assert_called_with({
        "food_items_from_image": {"image_path": image_path},
    })

