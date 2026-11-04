import pandas as pd


def read_csv(file):
    try:
        df = pd.read_csv(file)
        return df 
    except pd.errors.EmptyDataError as ex:
        raise  ValueError("CSV file is empty") from ex

    except pd.errors.ParserError as ex :
         raise ValueError("CSV file is defective") from ex


    