from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch


client = TestClient(app)

def test_upload_with_mock():
    with patch("routers.upload_router.save_air_quality") as mock_save:

        with open("air_quality_files/air_quality_2024_11_19.csv", "rb") as file:
            response = client.post(
                "/upload",
                files={"file": ("test.csv", file, "text/csv")}
            )

        assert response.status_code == 200
        mock_save.assert_called_once()        

def test_upload_missing_columns():
    csv_content = "date,city,PM2.5,NO2\n2024-11-21,Jerusalem,20,30"

    response = client.post(
        "/upload",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )

    assert response.json()["detail"] == "Missing required columns"
    assert response.status_code == 400        


def test_upload_no_valid_rows():
    csv_content = "date,city,PM2.5,NO2,CO2\n2024-11-21,Jerusalem,-20,30,400"    
    response = client.post(
        "/upload",
        files={"file": ("test.csv", csv_content, "text/csv")}
    )
    assert response.status_code == 400      