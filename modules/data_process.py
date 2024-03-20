import pandas as pd
import os
from langchain.tools import tool
import json
from typing import List
from langchain_core.agents import AgentActionMessageLog, AgentFinish
from langchain_core.pydantic_v1 import BaseModel, Field

PATH = "./data/"
NAME = "leads.csv"
DATAFRAME = pd.read_csv(os.path.join(PATH, NAME))


def if_exists(name: str) -> bool:
    names = list(DATAFRAME['Name'])
    if name in names:
        return True


def return_data(name: str) -> List[dict]:
    rows_with_element = DATAFRAME[DATAFRAME['Name'] == name]
    return rows_with_element.to_dict(orient='records')


@tool
def user_data():
    """Returns User Data"""
    return "Generate email from the provided data."


def parse(output):
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )


class Response(BaseModel):
    """Final responses to the question being asked and assessing the lead status"""
    agent: str = Field(description="The answer to query")
    status: str = Field(
        description="""Assess the lead if it has escalated or not.
            (Only 2 options Escalated or Not Escalated)"""
    )
