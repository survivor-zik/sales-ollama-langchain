import pandas as pd
import os
import json
from typing import List, Optional
from langchain.agents import tool
from langchain_core.agents import AgentFinish, AgentActionMessageLog
from langchain_core.pydantic_v1 import BaseModel, Field

PATH = "./data/"
NAME = "leads.csv"
DATAFRAME = pd.read_csv(os.path.join(PATH, NAME))
COLUMNS = [
    "Name",
    "Job Title",
    "Organizaton",
    "Company Size",
    "Department",
    "Project Title",
    "Looking For",
    "Lead Response",
]


def if_exists(name: str) -> bool:
    """
    Checks whether the Name exists or not.
    """
    names = list(DATAFRAME["Name"])
    if name in names:
        return True


def return_data(name: str) -> List[dict]:
    """Returns client's data"""
    data_frame = DATAFRAME[COLUMNS]
    rows_with_element = data_frame[data_frame["Name"] == name]
    return rows_with_element.to_dict(orient="records")


def return_model() -> tuple:
    """Returns a tuple from the dataframe which will serve as inputs"""
    model = DATAFRAME["Model"]
    temperature = DATAFRAME["Temperature"]
    opener = DATAFRAME["Opener"]
    escalator = DATAFRAME["Escalator"]
    return model[0], temperature[0], opener[0], escalator[0]


def add_value_to_column(column_name: str, index: int, value: Optional[str] = pd.NA) -> None:
    """Add values to an existing column or creates a new column with the value provided"""
    if column_name in DATAFRAME.columns:
        print(index," ",column_name,"column",value)
        DATAFRAME.loc[index, column_name] = value
    else:
        DATAFRAME[column_name] = None
        DATAFRAME.loc[index, column_name] = value


def find_index_by_name(name: str):
    """Returns index of the client being reached out."""
    try:
        index = DATAFRAME.index[DATAFRAME["Name"] == name].tolist()[0]
        return index
    except IndexError:
        print("Name not found.")
        return None


def save_file()-> None:
    """Saves file."""
    DATAFRAME.to_csv(os.path.join(PATH, NAME), index=False)


@tool
def user_data():
    """Returns User Data"""
    return "Generate email from the provided data."


def parse(output):
    """Parsing function to return desired format output"""
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
