from csv_reader import read_csv
from data_validator import validate_data
from pathlib import Path


def test_csv_validation():

    folder = Path("air_quality_files")

    for file in folder.glob("*.csv"):
        df = read_csv(file)
        k = len(df)
        print( validate_data(df))
        result = validate_data(df)
        assert len(result) <= k