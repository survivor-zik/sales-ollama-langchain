import pandas as pd
import os
from langchain.tools import tool
import json

from langchain_core.agents import AgentActionMessageLog, AgentFinish

PATH = "./data/"
NAME = "leads.csv"
DATAFRAME = pd.read_csv(os.path.join(PATH, NAME))


def if_exists(name: str) -> bool:
    names = list(DATAFRAME['Name'])
    if name in names:
        return True


def return_data(name: str) -> dict:
    rows_with_element = DATAFRAME[DATAFRAME['Name'] == name]
    return rows_with_element.to_dict(orient='records')


@tool
def user_data():
    """Returns User Data"""
    return " "


def parse(output):
    # If no function was invoked, return to user
    if "function_call" not in output.additional_kwargs:
        return AgentFinish(return_values={"output": output.content}, log=output.content)

    # Parse out the function call
    function_call = output.additional_kwargs["function_call"]
    name = function_call["name"]
    inputs = json.loads(function_call["arguments"])

    # If the Response function was invoked, return to the user with the function inputs
    if name == "Response":
        return AgentFinish(return_values=inputs, log=str(function_call))
    # Otherwise, return an agent action
    else:
        return AgentActionMessageLog(
            tool=name, tool_input=inputs, log="", message_log=[output]
        )
