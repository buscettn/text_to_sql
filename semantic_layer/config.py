from pathlib import Path

# Project structure paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LANCEDB_PATH = DATA_DIR / "lancedb"

# Embedding Configuration
# "ollama/" prefix tells LiteLLM to route this to your local Ollama instance
EMBEDDING_MODEL_NAME = "ollama/mxbai-embed-large:latest"
OLLAMA_API_BASE = "http://localhost:11434" # Default Ollama port
