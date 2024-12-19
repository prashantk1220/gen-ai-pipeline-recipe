import pytest
from fastapi.testclient import TestClient
from unittest import mock
from io import BytesIO
from whats_for_dinner.main import app


@pytest.fixture(autouse=True)
def mock_rag_pipeline():
    # Mock RagPipeline's query_recipe to avoid calling the actual method during tests
    with mock.patch("whats_for_dinner.main.rag_pipeline", autospec=True) as mock_pipeline:
        yield mock_pipeline


@pytest.fixture
def mock_image():
    # Create a mock image file (a small PNG image in memory)
    return BytesIO(b"fake image data")


@pytest.fixture
def client():
    return TestClient(app)


def test_recommend_recipe_with_ingredients(client, mock_rag_pipeline):
    ingredients = "tomato, cheese, pasta"

    mock_rag_pipeline.query_recipe.return_value = ["Mock recipe"]

    # Call the API with ingredients as form data
    response = client.post(
        "/recommend_recipe",
        data={"ingredients": ingredients}
    )

    # Assert the response is successful and the expected recipe is returned
    assert response.status_code == 200
    assert response.json() == "Mock recipe"

    # Ensure that the query_recipe method was called with the correct arguments
    mock_rag_pipeline.query_recipe.assert_called_once_with(ingredients, None)


def test_recommend_recipe_with_image(client, mock_rag_pipeline, mock_image):

    mock_rag_pipeline.query_recipe.return_value = ["Mock recipe"]

    # Mock image upload
    response = client.post(
        "/recommend_recipe",
        files={"image": ("test_image.png", mock_image, "image/png")}
    )

    # Assert the response is successful and the expected recipe is returned
    assert response.status_code == 200
    assert response.json() == "Mock recipe"

    # Ensure that the query_recipe method was called with the correct arguments
    mock_rag_pipeline.query_recipe.assert_called_once_with(None, mock.ANY)  # mock.ANY for the temporary file path


def test_recommend_recipe_missing_ingredients_and_image(client):
    # Call the API without ingredients or image
    response = client.post("/recommend_recipe")

    # Assert the response is a 400 error (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Provide ingredients as text or an image."}


