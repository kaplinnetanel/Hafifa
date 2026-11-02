import pandas as pd

def validate_data(df):
    valid_rows = []
    for index , row in df.iterrows():
        if has_missing_values(row):
            continue

        if has_ivalid_number(row):
            continue

        # if 

        # if 
        r = row.tolist()
        valid_rows.append(r)

    return valid_rows


def has_missing_values(row):


    value = pd.isna(row)
    if any(value):
        print(value[value].index)

        return True
    
    return False 

def has_ivalid_number(row):
    w = ["PM2.5", "NO2", "CO2"]

    result = True

    for ro in g:
        re = pd.to_numeric(row, errors="coerce")
        if re == false:
    

    return result