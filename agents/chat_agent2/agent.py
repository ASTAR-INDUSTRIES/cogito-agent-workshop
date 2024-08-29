from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.chat_agent2.utils.tools import tools
from agents.chat_agent2.utils.state import GraphState
from agents.chat_agent2.utils.nodes import chatbot, route_tools


workflow = StateGraph(GraphState)

workflow.add_node("chatbot", chatbot)
workflow.add_node("tools", ToolNode(tools=tools))

workflow.add_edge(START, "chatbot")
workflow.add_edge("tools", "chatbot")

workflow.add_conditional_edges(
    "chatbot",
    route_tools,
    {"tools": "tools", "__end__": END},
)

graph = workflow.compile()
