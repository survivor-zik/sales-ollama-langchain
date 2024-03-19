from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
# from langchain.chat_models import ChatOpenAI
#
# llm=ChatOpenAI()
# llm.bind
class Response(BaseModel):
    """Final response to the question being asked"""

    subject: str = Field(description="The subject of the email")
    body: str = Field(
        description="""The body of the email corresponding to the every individual
                     and designed distinctively for every individual."""
    )
