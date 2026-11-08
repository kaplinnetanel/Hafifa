import pytest
from processing.csv_reader import read_csv
from processing.data_validator import validate_data
from pathlib import Path
from processing.air_quality_processor import process_air_quality
from fastapi.testclient import TestClient
import pandas as pd

folder = Path("air_quality_files")
files = list(folder.glob("*.csv"))


@pytest.mark.parametrize("file", files)
def test_csv_validation(file):
    
    df = read_csv(file)
    valid_rows = validate_data(df)
    
    assert valid_rows is not None
    assert len(valid_rows) <= len(df)

    processed_rows = process_air_quality(valid_rows)
         
    for p in processed_rows:
        assert "aqi" in p
        assert "level" in p
        assert isinstance(p["aqi"], (int, float))

def test_date_format():
    df = pd.DataFrame([{
        "date": "11/21/2024",
        "city": "Jerusalem",
        "PM2.5": 20,
        "NO2": 30,
        "CO2": 400
    }])

    result = validate_data(df)

    assert result[0]["date"] == "2024-11-21"        