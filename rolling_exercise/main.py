from fastapi import FastAPI
from routers.upload_router import router as upload_router
from routers.air_quality_router import router as air_quality_router
from routers.alerts_router import router as alerts_router

from database.models import Base
from database.connection import engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


app.include_router(upload_router)
app.include_router(air_quality_router)
app.include_router(alerts_router)