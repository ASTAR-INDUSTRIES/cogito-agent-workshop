from agents.chat_agent1.utils.state import GraphState
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


llm = OpenAI(
    openai_api_key=os.getenv("COGITO_OPENAI_API_KEY"),
    )


def chatbot(state: GraphState):
    return {"messages": [llm.invoke(state["messages"])]}
