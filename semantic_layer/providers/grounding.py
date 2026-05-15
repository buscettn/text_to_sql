import os
import logging
from typing import List, Optional
from core.interfaces import ContextItem
from common.yaml_inheritance_loader import load_yaml_with_inheritance

logger = logging.getLogger(__name__)

# Base directory for grounding data
GROUNDING_DIR = os.path.join("data", "semantic_input", "grounding")

def _find_yaml_file(name: str, search_dir: str) -> Optional[str]:
    """Recursively search for a YAML file by name (without extension)."""
    if not os.path.exists(search_dir):
        logger.warning(f"Grounding directory not found: {search_dir}")
        return None
        
    for root, _, files in os.walk(search_dir):
        for file in files:
            if file.lower() == f"{name.lower()}.yaml" or file.lower() == f"{name.lower()}.yml":
                return os.path.join(root, file)
    return None

def get_grounding(query: str, domains: List[str]) -> List[ContextItem]:
    """
    Retrieves grounding context items based on identified domains and a global grounding file.
    
    Args:
        query: The user query (currently unused but kept for interface compatibility).
        domains: A list of domain names to load grounding for.
        
    Returns:
        A list of ContextItem objects containing grounding rules.
    """
    context_items = []
    
    # 1. Try to load global_grounding.yaml
    global_path = _find_yaml_file("global_grounding", GROUNDING_DIR)
    if global_path:
        try:
            data = load_yaml_with_inheritance(global_path)
            content = data.get("content")
            if content:
                context_items.append(ContextItem(
                    content=content, 
                    source="grounding", 
                    relevance_score=1.0, 
                    priority=1
                ))
            else:
                logger.warning(f"Global grounding file {global_path} has no 'content' attribute.")
        except Exception as e:
            logger.error(f"Error loading global grounding {global_path}: {e}")

    # 2. Load domain-specific YAMLs
    for domain in domains:
        domain_path = _find_yaml_file(domain, GROUNDING_DIR)
        if domain_path:
            try:
                data = load_yaml_with_inheritance(domain_path)
                content = data.get("content")
                if content:
                    context_items.append(ContextItem(
                        content=content, 
                        source="grounding", 
                        relevance_score=1.0, 
                        priority=1
                    ))
                else:
                    logger.warning(f"Grounding file for domain '{domain}' at {domain_path} has no 'content' attribute.")
            except Exception as e:
                logger.error(f"Error loading grounding for domain '{domain}' at {domain_path}: {e}")
        else:
            logger.debug(f"No grounding file found for domain '{domain}'.")

    return context_items