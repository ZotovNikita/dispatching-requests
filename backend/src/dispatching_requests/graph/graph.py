from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from .nodes import *


def graph_initialize(workflow: StateGraph) -> CompiledStateGraph:
    workflow.add_node('classification', email_classification)
    workflow.add_node('serial_number_check', serial_number_check)
    workflow.add_node('completeness_check', completeness_check)
    workflow.add_node('equipment_name_check', equipment_name_check)
    workflow.add_node('checks_inspection', checks_inspection)

    workflow.add_edge(START, 'classification')

    workflow.add_edge('classification', 'serial_number_check')
    workflow.add_edge('classification', 'completeness_check')
    workflow.add_edge('classification', 'equipment_name_check')

    workflow.add_edge(['serial_number_check', 'completeness_check', 'equipment_name_check'], 'checks_inspection')

    workflow.add_edge('checks_inspection', END)

    graph = workflow.compile()

    return graph
