write a simple yaml loader that allows to inherit yaml content from other files.
file should be /common/yaml_inheritance_loader.py

## API
The loader should provide the following entry point:
`def load_yaml_with_inheritance(file_path: str) -> dict:`

## Logic Description
when a yaml file is loaded it is loaded normally. if the top-level attribute "extends" is present and refers to a yaml file in the same folder (or subfolder when "subfolder/yamlname") the yaml mentioned is inherited. this means: all attributes that are not present in the original file are included as is from the base file.
when there are collisions (attribute in both files), the handling depends on whether the **top-level attribute** is in the **allowlist** (`content`, `prompt`, `examples`):
- **If in allowlist** (accumulative):
    - **Strings**: Concatenated (base + "\n\n" + original).
    - **Lists**: Appended (base + original).
    - **Dictionaries**: Deep merged (if keys collide within the dict, the original's value overwrites the base's value unless they are both dictionaries, in which case we recurse).
- **If NOT in allowlist** (overwriting):
    - The original attribute **overwrites** the base attribute entirely, regardless of type.

> [!NOTE]
> The allowlist check only applies to top-level keys. Nested attributes within a deep-merged dictionary do not trigger string concatenation or list appending; they follow standard deep-merge overwrite rules.

## Finalization
- The `extends` attribute must be **removed** from the final dictionary before returning.

## Error Handling
- **Circular Inheritance**: If a circular dependency is detected (e.g., A extends B, B extends A), the loader must raise a `ValueError` with a descriptive message.
- **Path Resolution**: 
    - Paths are relative to the directory of the file currently being loaded.
    - The loader should support `..` for parent directory traversal.
    - If the file is not found, the loader should try appending `.yaml` and `.yml` extensions automatically.

there are to file available for testing:
/data/semantic_input/grounding/domain1.yaml
/data/semantic_input/grounding/domainA_base.yaml

# Example:

#domain1.yaml:
domain: domain 1
description: some random description
extends: domainA_base
content: |
    This is some random content that is added after the domainA_base content.

#domainA_base.yaml:
domain: domain A
description: some random description of a base content
content: |
    This is some general content that is added.

loading domain1.yaml should result in:

#domain1.yaml:
domain: domain 1
description: some random description
content: |
    This is some general content that is added.

    This is some random content that is added after the domainA_base content.
