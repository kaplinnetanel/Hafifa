import pandas as pd
from logger import logger


def validate_data(df):
    valid_rows = []

    
    logger.info(f"Starting validation of {len(df)} rows")
    if has_missing_columns(df):
        logger.error("CSV validation failed: missing required columns")
        return None
    
    for index , row in df.iterrows():
        if has_missing_values(row):
            logger.warning(f"Row {index + 1}: missing values")
            continue

        if has_invalid_number(row):
            logger.warning(f"Row {index + 1}: invalid numeric value")
            continue

        if has_negative_values(row):
            logger.warning(f"Row {index + 1}: negative pollutant value")
            continue

        if has_invalid_date(row):
            logger.warning(f"Row {index + 1}: invalid date")
            continue

        if has_invalid_city(row):
            logger.warning(f"Row {index + 1}: invalid city")
            continue

        row["date"] = pd.to_datetime(row["date"]).date().isoformat()       
        for column in ["PM2.5", "NO2", "CO2"]:
            row[column] = float(row[column])

        
        valid_rows.append(row.to_dict())

    logger.info(f"Validation completed: {len(valid_rows)} valid rows")
    return valid_rows


def has_missing_columns(df):
    required_columns = ["date", "city", "PM2.5", "NO2", "CO2"]

    for  column in required_columns:
        if column not in df.columns:
            return True
        
    return False 


def has_missing_values(row):
    required_columns = ["date", "city", "PM2.5", "NO2", "CO2"]
    return row[required_columns].isna().any()

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