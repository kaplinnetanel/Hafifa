from fastapi import APIRouter,HTTPException
from database.repository import get_air_quality_by_date,get_air_quality_by_city,get_city_aqi_history,get_city_aqi_average,get_best_cities
from datetime import date

router = APIRouter(tags=["Air Quality"])

@router.get("/air-quality/date")
def get_air_by_date(start_date: date, end_date: date):
    if start_date > end_date:
        raise HTTPException(status_code= 400, detail= "start_date > end_date") 

    result_date = get_air_quality_by_date( start_date,end_date)

    if not result_date: 
        raise HTTPException(status_code= 404, detail= "dont ahve result" )
    
    return result_date

@router.get("/air-quality/city")
def get_city_data(city: str):
    city = city.strip()   
    if not city:
        raise HTTPException(status_code= 400, detail= "city is empty")
    
    result = get_air_quality_by_city(city)

    if not result:
        raise HTTPException(status_code= 404 , detail= "No data found")
    return result

@router.get("/city_aqi/history")
def get_city_history(city: str):
    city = city.strip()   
    if not city:
        raise HTTPException(status_code= 400, detail= "city is empty")
    
    result = get_city_aqi_history(city)

    if not result:
        raise HTTPException(status_code= 404 , detail= "No data found")
    return result

@router.get("/city_aqi/average")
def get_aqi_average(city: str):
    city = city.strip()   
    if not city:
        raise HTTPException(status_code= 400, detail= "city is empty")
    
    result = get_city_aqi_average(city)

    if result is None:
        raise HTTPException(status_code= 404 , detail= "No data found")
    return result

@router.get("/best_cities")
def get_cities():
    best_cities = get_best_cities()

    if not best_cities:
        raise HTTPException(status_code=404,detail="No data found")
    return best_cities
