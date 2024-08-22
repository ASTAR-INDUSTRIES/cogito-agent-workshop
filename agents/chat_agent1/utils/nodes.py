from agents.chat_agent1.utils.state import GraphState
from langchain_openai import AzureChatOpenAI

llm = AzureChatOpenAI()


def chatbot(state: GraphState):
    return {"messages": [llm.invoke(state["messages"])]}
