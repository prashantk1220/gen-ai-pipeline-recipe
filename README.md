# Recipe Recommendation Application

This is a proof-of-concept Python application that provides recipe recommendations based on user-provided ingredients, either as text or images. The application uses FastAPI for the API layer, a Haystack pipeline for retrieval, and integrates PostgreSQL with PGVector for efficient recipe storage and search.

## Features
- **Text-Based Recipe Search**: Input ingredients as plain text to find recipes.
- **Image-Based Recipe Search**: Upload an image of ingredients to extract visible food items and get recommendations.
- **Flexible Retrieval**: Uses embedding-based and keyword-based retrieval for accurate results.
- **Markdown-Formatted Results**: Recipe instructions are returned in Markdown format for readability.

## Tech Stack
- **Python**: Core programming language.
- **FastAPI**: Web framework for building the API.
- **Haystack**: NLP framework for retrieval-augmented generation (RAG).
- **PGVector**: Vector storage for similarity search.
- **OpenAI GPT-4o**: For text generation and image-based ingredient extraction.

## Installation

### Prerequisites
- Python 3.12+
- Docker & Docker Compose
- PostgreSQL database setup

### Setup Steps

1. **Clone the repository**
    ```bash
   git clone git@github.com:prashantk1220/gen-ai-pipeline-recipe.git
   cd gen-ai-pipeline-recipe
   ```

2. **Configure Environment Variables**
   Create a `.env` file with the following:
   ```env
   PG_CONN_STR=postgresql://<user>:<password>@<host>:<port>/<db_name>
   OPENAI_API_KEY=<your_openai_api_key>
   ```

3. **Set Up PostgreSQL with PGVector**
   Start PostgreSQL and App using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. **Or Build and Install the application locally**
    Make use of the Makefile provided with the helpful commands:
    ```bash
    make install
    ```

5. **Start the Application**
   ```bash
   make run
   ```
   OR
   ```bash
   OPENAI_API_KEY='key-here' PG_CONN_STR='db-url' make run
   ```

6. **Access the API**
   Visit `http://127.0.0.1:8080/` for the interactive API documentation.

## API Endpoints

### **POST /recommend_recipe**
- **Description**: Provides recipe recommendations based on input ingredients.
- **Parameters**:
  - `ingredients`: (optional) List of ingredients as text.
  - `image`: (optional) An image of ingredients.
- **Response**: Recommended recipes with instructions in Markdown format.

**Example Requests**:

1. **Text-Based Search**:
   ```bash
   curl -X 'POST' \
   'http://127.0.0.1:8080/recommend_recipe' \
   -H 'accept: application/json' \
   -H 'Content-Type: multipart/form-data' \
   -F 'ingredients=tomato, onion, garlic' 
   ```

2. **Image-Based Search**:
   ```bash
   curl -X 'POST' \
   'http://127.0.0.1:8080/recommend_recipe' \
   -H 'accept: application/json' \
   -H 'Content-Type: multipart/form-data' \
   -F 'image=@food4.webp;type=image/webp'
   ```
   
It can also be tried out from the swagger documentation provided at `http://127.0.0.1:8080/docs`

## Testing

### Running Tests
   Unit tests are included for both the query processor and the API. Use `pytest` to run them:
   ```bash
     make tests
   ```

## System Architecture

Below is the high-level system architecture of the project. 
![System Architecture](../docs/system-architecture.png)


Makefile Commands 
-----------------

The `Makefile` simplifies common tasks for this project. Below is a list of the most important commands:

| Command          | Description                                     |
|------------------|-------------------------------------------------|
| `make clean`     | Remove Python cache files and test artifacts.   |
| `make clean-all` | Remove venv dir and then cleans                 |
| `make install`   | Install all required dependencies using Poetry. |
| `make tests`     | Run the test suite using `pytest`.              |
| `make run`       | Launch the FastAPI application.                 |
| `make all`       | Runs all the above cmds in sequence.            |
| `make help`      | Display the commands available.                 |

## Future Improvements
- Packages can be introduced to group similar functionality modules into same package
- Enhance image processing for faster detection
- Integrate a front-end UI for a better user experience.
