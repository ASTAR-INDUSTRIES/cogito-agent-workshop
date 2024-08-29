from agents.chat_agent2.utils.state import GraphState
from agents.chat_agent2.utils.tools import tools
from langchain_openai import ChatOpenAI
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

llm_with_tools = ChatOpenAI(
    openai_api_key=os.getenv("COGITO_OPENAI_API_KEY"),
    ).bind_tools(tools)


def chatbot(state: GraphState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


def route_tools(
    state: GraphState,
) -> Literal["tools", "__end__"]:
    """
    Use in the conditional_edge to route to the ToolNode if the last message
    has tool calls. Otherwise, route to the end.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "__end__"
