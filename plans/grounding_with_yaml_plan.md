# grounding with yaml
(primarily affects grounding.py provider and grounding node)
the goal is to based on the domains received to load yamls from /data/semantic_input/grounding/

first it must be ensured that the grounding provider works with multiple domains.
The function `get_grounding` in `semantic_layer/providers/grounding.py` shall be updated to accept a list of domains: `get_grounding(query: str, domains: List[str]) -> List[ContextItem]`.

the query parameter shall be kept in place but has no function at the moment.

additionally, always try to load "global_grounding.yaml".
if it doesn't exist, ignore it.

for every domain: search recursively in "/data/semantic_input/grounding/" for the corresponding yaml (domain name = yaml name.yaml).
if multiple files with the same name exist, log a warning and use the first one found.
if there is no domain yaml: ignore it.
if the yaml exists but has no "content" attribute: log a warning and ignore it.

return all read grounding-yamls, each as a context item. 
The global grounding context (if available) must be the first item in the returned list.
The "content" field of the ContextItem should strictly contain the string from the "content" attribute of the merged YAML.
priority is 1, relevance_score is 1.
source is "grounding".


## miscellaneous
when loading yamls use the /common/yaml_inheritance_loader.py