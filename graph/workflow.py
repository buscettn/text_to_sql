from langgraph.graph import StateGraph, END
from core.state import TextToSQLState
from graph.nodes.intent_node import intent_node
from graph.nodes.domain_mapping_node import domain_mapping_node
from graph.nodes.schema_retrieval_node import schema_retrieval_node
from graph.nodes.dynamic_few_shot_retrieval_node import dynamic_few_shot_retrieval_node
from graph.nodes.grounding_node import grounding_node
from graph.nodes.pre_generation_node import pre_generation_node
from graph.nodes.generator_node import generator_node
from graph.nodes.validator_node import validator_node

def create_workflow():
    workflow = StateGraph(TextToSQLState)

    workflow.add_node("intent_guard", intent_node)
    workflow.add_node("domain_mapping", domain_mapping_node)
    workflow.add_node("schema_retrieval", schema_retrieval_node)
    workflow.add_node("dynamic_few_shot_retrieval", dynamic_few_shot_retrieval_node)
    workflow.add_node("grounding", grounding_node)
    workflow.add_node("pre_generation", pre_generation_node)
    workflow.add_node("generator", generator_node)
    workflow.add_node("validator", validator_node)

    workflow.set_entry_point("intent_guard")
    workflow.add_edge("intent_guard", "domain_mapping")
    workflow.add_edge("domain_mapping", "schema_retrieval")
    workflow.add_edge("schema_retrieval", "dynamic_few_shot_retrieval")
    workflow.add_edge("dynamic_few_shot_retrieval", "grounding")
    workflow.add_edge("grounding", "pre_generation")
    workflow.add_edge("pre_generation", "generator")
    workflow.add_edge("generator", "validator")
    workflow.add_edge("validator", END)

    return workflow.compile()