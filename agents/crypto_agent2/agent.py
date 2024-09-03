from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from agents.crypto_agent2.utils.tools import python_repl
from agents.crypto_agent2.utils.state import GraphState
from agents.crypto_agent2.utils.nodes import crypto_agent, create_api_call, retrieve_data_from_api, router, generate, route_tools

workflow = StateGraph(GraphState)

workflow.add_node("crypto_agent", crypto_agent)
workflow.add_node("create_api_call", create_api_call)
workflow.add_node("retrieve_data_from_api", retrieve_data_from_api)
workflow.add_node("generate", generate)
workflow.add_node("python_repl", ToolNode([python_repl]))

workflow.add_edge(START, "crypto_agent")
workflow.add_edge("create_api_call", "retrieve_data_from_api")
workflow.add_edge("retrieve_data_from_api", "crypto_agent")
workflow.add_edge("python_repl", "generate")

workflow.add_conditional_edges(
    "crypto_agent",
    router,
    {
        "create_api_call": "create_api_call",
        "generate": "generate"
    }
)

workflow.add_conditional_edges(
    "generate",
    route_tools,
    {
        "python_repl": "python_repl",
        "__end__": END
    }
)

graph = workflow.compile()
