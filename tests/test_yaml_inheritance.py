import sys
import os
import pytest

# Add the project root to sys.path to allow importing from common
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.yaml_inheritance_loader import load_yaml_with_inheritance

def test_inheritance_example():
    # Paths from the plan
    domain1_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/semantic_input/grounding/domain1.yaml'))
    
    # Load domain1.yaml
    result = load_yaml_with_inheritance(domain1_path)
    
    # Expected results from the plan:
    # domain: domain 1
    # description: some random description
    # content: (concatenated)
    
    assert result['domain'] == 'domain 1'
    assert result['description'] == 'some random description'
    assert "This is some general content that is added." in result['content']
    assert "This is some random content that is added after the domainA_base content." in result['content']
    assert "\n\n" in result['content'] # Check for double newline separator
    assert 'extends' not in result

def test_circular_inheritance():
    # Create temp circular files
    file_a = "temp_a.yaml"
    file_b = "temp_b.yaml"
    
    with open(file_a, "w") as f:
        f.write("extends: temp_b\nattr: a")
    with open(file_b, "w") as f:
        f.write("extends: temp_a\nattr: b")
        
    try:
        with pytest.raises(ValueError, match="Circular inheritance detected"):
            load_yaml_with_inheritance(file_a)
    finally:
        if os.path.exists(file_a): os.remove(file_a)
        if os.path.exists(file_b): os.remove(file_b)

def test_deep_merge_allowlist():
    # Test dictionary merging in allowlist (using 'examples' which is in ALLOWLIST)
    file_base = "temp_base.yaml"
    file_child = "temp_child.yaml"
    
    with open(file_base, "w") as f:
        f.write("examples:\n  nested1: base_val\n  nested2: base_val")
    with open(file_child, "w") as f:
        f.write("extends: temp_base\nexamples:\n  nested2: child_val\n  nested3: child_val")
        
    try:
        result = load_yaml_with_inheritance(file_child)
        assert result['examples']['nested1'] == 'base_val'
        assert result['examples']['nested2'] == 'child_val'
        assert result['examples']['nested3'] == 'child_val'
    finally:
        if os.path.exists(file_base): os.remove(file_base)
        if os.path.exists(file_child): os.remove(file_child)

def test_overwrite_non_allowlist():
    # Test that dicts NOT in allowlist are overwritten
    file_base = "temp_base.yaml"
    file_child = "temp_child.yaml"
    
    with open(file_base, "w") as f:
        f.write("metadata:\n  author: admin\n  version: 1")
    with open(file_child, "w") as f:
        f.write("extends: temp_base\nmetadata:\n  version: 2")
        
    try:
        result = load_yaml_with_inheritance(file_child)
        # Should NOT contain author: admin because metadata is not in ALLOWLIST
        assert result['metadata'] == {'version': 2}
    finally:
        if os.path.exists(file_base): os.remove(file_base)
        if os.path.exists(file_child): os.remove(file_child)

if __name__ == "__main__":
    # Run tests if called directly
    pytest.main([__file__])
