from typing_extensions import TypedDict, List, Literal
from langgraph.graph.message import add_messages
from typing import Annotated
from pydantic import BaseModel, Field

class route(BaseModel):
    step: Literal["tool","sql"]=Field(description="The next step in the routing process")