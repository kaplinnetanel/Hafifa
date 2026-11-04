from fastapi import APIRouter, UploadFile, File ,HTTPException
from database.repository import save_air_quality
from processing.csv_reader import read_csv
from processing.data_validator import validate_data
from processing.air_quality_processor import process_air_quality
from logger import logger

router = APIRouter(tags=["Upload"])

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    logger.info(f"Uploading file: {file.filename}")
    try:
        df = read_csv(file.file)

    except ValueError as ex:
        logger.error(f"Failed to read file {file.filename}: {ex}")
        raise HTTPException(status_code=400, detail=str(ex)) from ex
        
    valid_rows = validate_data(df)

    if valid_rows is None:
        logger.error(f"File {file.filename}: Missing required columns")
        raise HTTPException(status_code=400,detail="Missing required columns")

    if not valid_rows:
        logger.error(f"File {file.filename}: No valid rows found")
        raise HTTPException(status_code=400,detail="No valid rows found")
    
    processed_rows = process_air_quality(valid_rows)
    save_air_quality(processed_rows)

    logger.info(f"File {file.filename} saved successfully. " f"Saved {len(processed_rows)} rows")

    return {"filename": file.filename}
