import os
from pathlib import Path
from whats_for_dinner.documents_store import DocumentsStore


class Ingestion:
    """
    This module handles data ingestion into the PgVector Document Store
    """

    def __init__(self, documents_store: DocumentsStore):
        self.documents_store = documents_store

    def ingest_recipes(self, folder_path: Path):
        """
        Ingest all recipes from text files in the specified folder into the database and document store.
        :param folder_path: Path to the folder containing recipe text files.
        """
        recipes = []

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".txt"):
                recipe = self.parse_recipe_file(os.path.join(folder_path, file_name))
                recipes.append(recipe)

        # Save to document store
        docs = self.documents_store.load_recipes_to_store(recipes)
        print(docs)


    @staticmethod
    def parse_recipe_file(file_path: str):
        """
        Parse a recipe from a text file.
        :param file_path: Path to the recipe text file.
        :return: A dictionary containing title, ingredients, and instructions.
        """
        with open(file_path, "r") as file:
            lines = file.readlines()
            title = lines[0].strip()
            ingredients_start = lines.index("Ingredients:\n") + 1
            instructions_start = lines.index("Instructions:\n") + 1

            ingredients = "".join(lines[ingredients_start:instructions_start - 1]).strip()
            instructions = "".join(lines[instructions_start:]).strip()

            return {
                "title": title,
                "ingredients": ingredients,
                "instructions": instructions,
            }




