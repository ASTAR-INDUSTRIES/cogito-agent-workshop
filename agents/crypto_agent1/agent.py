from langgraph.graph import StateGraph, START, END
from agents.crypto_agent1.utils.state import GraphState
from agents.crypto_agent1.utils.nodes import crypto_agent, create_api_call, retrieve_data_from_api, router, generate

workflow = StateGraph(GraphState)

workflow.add_node("crypto_agent", crypto_agent)
workflow.add_node("create_api_call", create_api_call)
workflow.add_node("retrieve_data_from_api", retrieve_data_from_api)
workflow.add_node("generate", generate)

workflow.add_edge(START, "crypto_agent")
workflow.add_edge("create_api_call", "retrieve_data_from_api")
workflow.add_edge("retrieve_data_from_api", "crypto_agent")
workflow.add_edge("generate", END)

workflow.add_conditional_edges(
    "crypto_agent",
    router,
    {
        "create_api_call": "create_api_call",
        "generate": "generate"
    }
    )

graph = workflow.compile()
