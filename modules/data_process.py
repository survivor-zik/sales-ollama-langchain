import pandas as pd
import os

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
