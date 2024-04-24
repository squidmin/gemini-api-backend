from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware

import os

from google.cloud import secretmanager
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

app = FastAPI()

origins = [
    "http://localhost:3000",  # Frontend address
    "https://example.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins (use ["*"] for all origins)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
api_key_secret_name = os.getenv("GEMINI_API_KEY_SECRET_NAME")
if not project_id or not api_key_secret_name:
    raise HTTPException(status_code=400, detail="Project ID or API Key Secret Name is not set.")


@app.get("/list-models/")
def list_models():
    api_key = get_api_key()
    if not api_key:
        raise HTTPException(status_code=400, detail="Failed to retrieve API Key.")
    genai.configure(api_key=api_key)
    models_supporting_generation = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models_supporting_generation.append(m.name)
        return models_supporting_generation
    except Exception as e:
        # This could be a network error, configuration issue, etc.
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/generate-text/")
async def generate_text(prompt: str = Query(..., description="The prompt to generate text for")):
    # print(await request.json())  # For debugging; shows the raw JSON body
    api_key = get_api_key()
    if not api_key:
        raise HTTPException(status_code=400, detail="Failed to retrieve API Key.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    content = model.generate_content(prompt).text
    # Assuming `generate_content` returns a string or a structure that can be directly converted to JSON
    return {"generated_text": content}


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def get_api_key():
    """Fetches API key from Google Cloud Secrets Manager."""
    name = f"projects/{project_id}/secrets/{api_key_secret_name}/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
