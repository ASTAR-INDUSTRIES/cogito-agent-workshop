from typing import TypedDict, Annotated, Literal
from langgraph.graph.message import add_messages
from langchain_core.pydantic_v1 import BaseModel, Field


class ApiCall(BaseModel):
    url: str = Field(..., description="The URL to call")
    method: str = Field("GET", description="The HTTP method to use")
    headers: dict = Field({}, description="The headers to send")
    body: dict = Field({}, description="The body to send")


class GraphState(TypedDict):
    api_call: ApiCall
    messages: Annotated[list, add_messages]
    decision: Literal["create_api_call", "generate"]
    data: dict
