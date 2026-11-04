from fastapi import APIRouter,HTTPException
from database.repository import get_all_alerts,get_alerts_by_date,get_alerts_by_city
from datetime import date

router = APIRouter(tags=["Alerts"])

@router.get("/alerts")
def get_alerts():
    alerts = get_all_alerts()

    if not alerts:
        raise HTTPException(status_code= 404, detail= "Not data found")

    return alerts

@router.get("/alerts/date")
def get_alerts_date(date: date):
    alerts = get_alerts_by_date(date)

    if not alerts:
        raise HTTPException(status_code=404, detail="No alerts found")

    return alerts


@router.get("/alerts/city")
def get_alerts_city(city: str):
    city = city.strip()

    if not city:
        raise HTTPException(status_code=400, detail="City is empty")

    alerts = get_alerts_by_city(city)

    if not alerts:
        raise HTTPException(status_code=404, detail="No alerts found")

    return alerts