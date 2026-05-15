import yaml
import os
from typing import Any, Dict, List, Set, Optional

ALLOWLIST = {"content", "prompt", "examples"}

def _deep_merge(base: Dict[str, Any], original: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standard deep merge for dictionaries.
    The original's value overwrites the base's value unless they are both dictionaries.
    """
    merged = base.copy()
    for key, value in original.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged

def _merge_logic(base: Dict[str, Any], original: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply the plan's merge logic based on the top-level allowlist.
    """
    # 1. Start with all attributes from base
    result = base.copy()
    
    # 2. Iterate through original attributes to merge or overwrite
    for key, value in original.items():
        if key == "extends":
            continue
            
        if key in result:
            # Collision handling
            if key in ALLOWLIST:
                # Accumulative logic
                base_val = result[key]
                if isinstance(base_val, str) and isinstance(value, str):
                    result[key] = f"{base_val}\n\n{value}"
                elif isinstance(base_val, list) and isinstance(value, list):
                    result[key] = base_val + value
                elif isinstance(base_val, dict) and isinstance(value, dict):
                    result[key] = _deep_merge(base_val, value)
                else:
                    # Type mismatch in allowlist? Default to original overwrite
                    result[key] = value
            else:
                # Overwriting logic (NOT in allowlist)
                result[key] = value
        else:
            # New attribute in original (not in base)
            result[key] = value
            
    return result

def load_yaml_with_inheritance(file_path: str, _seen_files: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Loads a YAML file and recursively resolves inheritance via the 'extends' attribute.
    
    Args:
        file_path: Path to the YAML file to load.
        _seen_files: Internal list for circular inheritance detection.
        
    Returns:
        A dictionary containing the merged YAML content.
        
    Raises:
        ValueError: If a circular inheritance is detected.
        FileNotFoundError: If the YAML file or its parents cannot be found.
    """
    # Determine the actual path (handle missing extensions)
    if not os.path.exists(file_path):
        found = False
        for ext in [".yaml", ".yml"]:
            if os.path.exists(file_path + ext):
                file_path = file_path + ext
                found = True
                break
        if not found:
            raise FileNotFoundError(f"YAML file not found: {file_path}")

    abs_path = os.path.abspath(file_path)
    
    if _seen_files is None:
        _seen_files = []
        
    if abs_path in _seen_files:
        cycle = " -> ".join(_seen_files + [abs_path])
        raise ValueError(f"Circular inheritance detected: {cycle}")
        
    _seen_files.append(abs_path)
    
    # Load the current file
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f) or {}

    if "extends" in content and content["extends"]:
        extends_path = content["extends"]
        # Resolve path relative to current file's directory
        current_dir = os.path.dirname(abs_path)
        base_file_path = os.path.join(current_dir, extends_path)
        
        # Recursive load base file (pass a copy of seen files to avoid branch pollution)
        base_content = load_yaml_with_inheritance(base_file_path, _seen_files.copy())
        
        # Merge base into original (original's values take precedence or accumulate)
        final_content = _merge_logic(base_content, content)
    else:
        final_content = content.copy()

    # Ensure 'extends' is removed from final result
    final_content.pop("extends", None)
    
    return final_content
