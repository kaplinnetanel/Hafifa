from sqlalchemy.orm import Session 
from database.connection import engine
from database.models import AirQuality, Alerts
from datetime import date
from sqlalchemy import select ,func
import os
from dotenv import load_dotenv

load_dotenv()

ALERT_AQI_THRESHOLD = int(os.getenv("ALERT_AQI_THRESHOLD", "300"))

def save_air_quality(rows):
    with Session(engine) as session :
        for row in rows:
            parsed_date = date.fromisoformat(row["date"])
            record = AirQuality(
                date = parsed_date,
                city =  row["city"],
                pm25 = row["PM2.5"],
                no2 =  row["NO2"],
                co2 =  row["CO2"],
                aqi = row["aqi"],
                level = row["level"]
            )
            session.add(record)

            if row["aqi"] > ALERT_AQI_THRESHOLD:
                alert = Alerts( 
                    date = parsed_date,
                    city =  row["city"],
                    aqi = row["aqi"]
                )
                session.add(alert)  
        
        session.commit()

def get_air_quality_by_date(start_date, end_date):
    with Session (engine) as session:
        query  = select(AirQuality).where(AirQuality.date.between(start_date, end_date))
        result = session.scalars(query).all()
        return result
      
def get_air_quality_by_city(city : str):

    with Session (engine) as session:
        query  = select(AirQuality).where(AirQuality.city == city)
        result = session.scalars(query).all()
        return result

def get_city_aqi_history(city: str):
    with Session (engine) as session:
            query  = select(AirQuality.aqi, AirQuality.date).where(AirQuality.city == city).order_by(AirQuality.date)
            result = session.execute(query).all()
            return result
def get_city_aqi_average(city: str):
    with Session(engine) as session:
        query = select(func.avg(AirQuality.aqi)).where(
            AirQuality.city == city
        )

        return session.scalar(query)

def get_best_cities():
     with Session (engine) as session:
            query  = select(AirQuality.city, func.min(AirQuality.aqi)).group_by(AirQuality.city).order_by(func.min(AirQuality.aqi)).limit(3) 
            result = session.execute(query).mappings().all()
            return result

def get_all_alerts():
    with Session (engine) as session:
        query  = select(Alerts)
        result = session.scalars(query).all()
        return result

def get_alerts_by_date(date):
    with Session(engine) as session:
        query = select(Alerts).where(Alerts.date == date)
        result = session.scalars(query).all()
        return result


def get_alerts_by_city(city: str):
    with Session(engine) as session:
        query = select(Alerts).where(Alerts.city == city)
        result = session.scalars(query).all()
        return result