from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class Response(BaseModel):
    """Final response to the question being asked"""
    subject: str = Field(description="The subject of the email")
    body: str = Field(
        description="""The body of the email corresponding to the every individual
                     and designed distinctively for every individual."""
    )


class Response_Esc(BaseModel):
    """Final response to the question being asked"""
    agent_response: str = Field(description="The subject of the email")
    lead_status: str = Field(
        description="""The body of the email corresponding to the every individual
                     and designed distinctively for every individual."""
    )
