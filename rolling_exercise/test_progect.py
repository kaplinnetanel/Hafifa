from processing.csv_reader import read_csv
from processing.data_validator import validate_data
from pathlib import Path
from processing.air_quality_processor import process_air_quality

def test_csv_validation():
    folder = Path("air_quality_files")
    files = list(folder.glob("*.csv"))

    assert files, "No CSV files found"

    for file in files:
        df = read_csv(file)
        valid_rows = validate_data(df)
        processed_rows = process_air_quality(valid_rows)

       
        assert valid_rows is not None
        assert len(valid_rows) <= len(df)
        
        print(f"{file.name}: {len(valid_rows)}/{len(df)} valid rows")
        for p in processed_rows:
             print(p["level"],p["aqi"])