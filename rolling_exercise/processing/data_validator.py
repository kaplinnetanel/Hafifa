import pandas as pd

def validate_data(df):
    valid_rows = []

    if has_missing_columns(df):
        return None
    
    for index , row in df.iterrows():
        if has_missing_values(row):
            continue

        if has_invalid_number(row):
            continue

        if has_negative_values(row):
            continue

        if has_invalid_date(row):
            continue

        if has_invalid_city(row):
            continue

        valid_rows.append(row.to_dict())

    return valid_rows


def has_missing_columns(df):
    required_columns = ["date", "city", "PM2.5", "NO2", "CO2"]

    for  column in required_columns:
        if column not in df.columns:
            return True
        
    return False 


def has_missing_values(row):

    value = pd.isna(row)
    if any(value):
        print(value[value].index)

        return True
    
    return False 

def has_invalid_number(row):

    columns = ["PM2.5", "NO2", "CO2"]

    for column in columns:
        value = pd.to_numeric(row[column],errors= "coerce")

        if pd.isna(value):
            return True
        
    return False

def has_negative_values(row):
    columns =  ["PM2.5", "NO2", "CO2"]

    for column in columns:
        if float(row[column]) < 0 :
            return True

    return False     

def has_invalid_date(row):

    value = pd.to_datetime(row["date"],errors= "coerce")

    if pd.isna(value):
        return True
    
    return False

def has_invalid_city(row):
    city = row["city"]
    if not isinstance(city,str):
        return True
    clean_city = city.strip()

    if not clean_city:
        return True
    return False