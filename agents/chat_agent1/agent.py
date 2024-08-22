
from langgraph.graph import StateGraph, START, END
from utils.state import GraphState

workflow = StateGraph(GraphState)

workflow.add_edge(START, END)

graph = workflow.compile()
