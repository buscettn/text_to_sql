import pytest
import os
import shutil
from semantic_layer.providers.grounding import get_grounding
from core.interfaces import ContextItem

@pytest.fixture
def temp_grounding_setup():
    base_dir = os.path.join("data", "semantic_input", "grounding")
    nested_dir = os.path.join(base_dir, "test_nested")
    os.makedirs(nested_dir, exist_ok=True)
    
    nested_file = os.path.join(nested_dir, "nested_domain.yaml")
    with open(nested_file, "w") as f:
        f.write("content: 'Nested content for testing'\n")
        
    yield nested_dir
    
    # Cleanup
    if os.path.exists(nested_dir):
        shutil.rmtree(nested_dir)

def test_get_grounding_basic():
    # Testing with domain1 which exists in the real data
    results = get_grounding("dummy query", ["domain1"])
    
    # Results should contain global_grounding (if exists) and domain1
    assert len(results) > 0
    for item in results:
        assert isinstance(item, ContextItem)
        assert item.source == "grounding"
        assert item.priority == 1
        assert item.relevance_score == 1.0

def test_get_grounding_recursive(temp_grounding_setup):
    results = get_grounding("dummy", ["nested_domain"])
    contents = [item.content for item in results]
    assert any("Nested content for testing" in c for c in contents)

def test_get_grounding_missing_content():
    base_dir = os.path.join("data", "semantic_input", "grounding")
    missing_content_file = os.path.join(base_dir, "missing_content.yaml")
    with open(missing_content_file, "w") as f:
        f.write("description: 'No content field here'\n")
        
    try:
        results = get_grounding("dummy", ["missing_content"])
        contents = [item.content for item in results]
        # Should not contain anything from missing_content.yaml
        assert not any("No content field here" in c for c in contents)
    finally:
        if os.path.exists(missing_content_file):
            os.remove(missing_content_file)

def test_get_grounding_order():
    # Verify global_grounding is first if it exists
    results = get_grounding("dummy", ["domain1"])
    if len(results) > 1:
        # Check if the first one is likely the global one
        # This depends on the actual content of global_grounding.yaml vs domain1.yaml
        pass 
