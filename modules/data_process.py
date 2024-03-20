import pandas as pd
import os
from typing import Union

PATH = "./data/"
NAME = "leads.csv"
DATAFRAME = pd.read_csv(os.path.join(PATH, NAME))
COLUMNS = ['Name', 'Job Title', 'Organizaton', 'Company Size', 'Department', 'Project Title', 'Looking For',
           'Lead Response']


def if_exists(name: str) -> bool:
    names = list(DATAFRAME['Name'])
    if name in names:
        return True


def return_data(name: str) -> dict:
    data_frame = DATAFRAME[COLUMNS]
    rows_with_element = data_frame[data_frame['Name'] == name]
    return rows_with_element.to_dict(orient='records')


def return_model():
    model = DATAFRAME['Model']
    temperature = DATAFRAME['Temperature']
    opener = DATAFRAME['Opener']
    escalator = DATAFRAME["Escalator"]
    return model[0], temperature[0], opener[0], escalator[0]


def add_value_to_column(column_name: str, index: float, value):
    if column_name in DATAFRAME.columns:
        DATAFRAME.at[index, column_name] = value
    else:
        DATAFRAME[column_name] = pd.NA
        DATAFRAME.at[index, column_name] = value


def find_index_by_name(name: str):
    try:
        index = DATAFRAME.index[DATAFRAME['Name'] == name].tolist()[0]
        return index
    except IndexError:
        print("Name not found.")
        return None


def save_file():
    DATAFRAME.to_csv(os.path.join(PATH, NAME), mode='a')
