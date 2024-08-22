
from langgraph.graph import StateGraph, START, END
from agents.chat_agent1.utils.state import GraphState
from agents.chat_agent1.utils.nodes import chatbot

workflow = StateGraph(GraphState)

workflow.add_node("chatbot", chatbot)

workflow.add_edge(START, "chatbot")
workflow.add_edge("chatbot", END)


graph = workflow.compile()
