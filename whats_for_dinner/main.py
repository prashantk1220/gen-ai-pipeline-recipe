import os
import tempfile
from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Form, UploadFile, HTTPException
from fastapi.responses import RedirectResponse

from whats_for_dinner.documents_store import DocumentsStore
from whats_for_dinner.ingestion import Ingestion
from whats_for_dinner.rag_pipeline import RagPipeline
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Shared RagPipeline instance
rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    BASE_DIR = Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parent.parent))
    recipes_path = BASE_DIR / "data" / "recipes"
    documents_store = DocumentsStore()
    if os.getenv("LOAD_DATA_ON_STARTUP", "false").lower() == "true":
        ingestion = Ingestion(documents_store)
        ingestion.ingest_recipes(recipes_path)
    global rag_pipeline
    rag_pipeline = RagPipeline(documents_store.document_store)

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/recommend_recipe")
def recommend_recipe(
        ingredients: str = Form(None),
        image: UploadFile = None
):
    """
    Recommends recipes based on ingredients provided as text or image.
    """
    if not ingredients and not image:
        raise HTTPException(status_code=400, detail="Provide ingredients as text or an image.")

    image_path = None
    if image:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(image.file.read())
            image_path = temp_file.name

    try:
        result = rag_pipeline.query_recipe(ingredients, image_path)
        if not result:
            raise HTTPException(status_code=404, detail="No matching recipes found")
        return result[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if image_path:
            os.remove(image_path)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")


def start_app(*args, **kwargs):
    host = kwargs.get('host', '127.0.0.1')
    port = kwargs.get('port', 8080)
    uvicorn.run(app, host=host, port=port)
