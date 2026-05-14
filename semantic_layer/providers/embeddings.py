from litellm import embedding
from semantic_layer.config import EMBEDDING_MODEL_NAME, OLLAMA_API_BASE

def get_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector using LiteLLM and Ollama.
    Uses centralized configuration from semantic_layer.config.
    """
    response = embedding(
        model=EMBEDDING_MODEL_NAME,
        input=text,
        api_base=OLLAMA_API_BASE
    )
    # Extract the vector from the LiteLLM response payload
    return response['data'][0]['embedding']
