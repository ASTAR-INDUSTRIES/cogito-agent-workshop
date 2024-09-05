from agents.crypto_agent2.utils.state import GraphState, ApiCall
from agents.crypto_agent2.utils.tools import python_repl
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Literal
import requests
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    openai_api_key=os.getenv("COGITO_OPENAI_API_KEY"),
    model_name="gpt-4o-mini",
    )

tools = [python_repl]


def crypto_agent(state: GraphState):
    """Agent to determine what to do"""
    prompt = PromptTemplate(
        template="""
        You are a crypto expert and will help the user with their crypto questions.
        The message history is the following:

        Messages: {messages}

        And data gathered so far is the following:

        Data: {data}

        You have the following options:

        1. 'create_api_call': Create an API call (Use the CoinGecko API to retrieve data)
        2. 'generate': Generate a response if you have what you need to answer

        Answer with just the option name and nothing else.
        """,
    )
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"messages": state["messages"], "data": state.get("data", {})})
    return {"decision": response}


def router(state: GraphState) -> Literal["create_api_call", "generate"]:
    """Router to determine what to do"""
    return state["decision"]


def create_api_call(state: GraphState):
    """Creates an API call to retrieve the necessary data"""
    prompt = PromptTemplate(
        template="""
        Your job is to create an API call to retrieve data from the CoinGecko API.
        The call should retrieve data to help answer the user's question.

        The message history is the following:

        Messages: {messages}

        And data gathered so far is the following:

        Data: {data}

        Please create an API call to retrieve the necessary data.
        """,
    )
    chain = prompt | llm.with_structured_output(ApiCall)
    response = chain.invoke({"messages": state["messages"], "data": state.get("data", {})})
    return {"api_call": response}


def retrieve_data_from_api(state: GraphState):
    """Retrieves data from an API"""
    api_call = state["api_call"]
    response = requests.request(
        method=api_call.method,
        url=api_call.url,
        headers=api_call.headers,
        data=api_call.body,
    )
    return {"data": response.json()}


def generate(state: GraphState):
    """Generates a response based on question asked by user and the data gathered"""
    prompt = PromptTemplate(
        template="""
        You are a crypto expert and will help the user with their crypto questions.

        The message history is the following:

        Messages: {messages}

        And data gathered so far is the following:

        Data: {data}

        Your job is to formulate a response that answers the user's question.
        You should always try to return good visual data graphics to help the user understand better.
        """,
    )
    chain = prompt | llm.bind_tools(tools=tools)
    response = chain.invoke({"messages": state["messages"], "data": state.get("data", {})})
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
