from agents.chat_agent1.utils.state import GraphState
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


llm = AzureChatOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        model=os.getenv("AZURE_OPENAI_MODEL"),
        api_version=os.getenv("AZURE_OPENAI_VERSION"),
        temperature=0
    )


def chatbot(state: GraphState):
    return {"messages": [llm.invoke(state["messages"])]}
