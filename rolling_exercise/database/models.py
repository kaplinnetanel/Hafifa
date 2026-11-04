from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date as d
from sqlalchemy import String

class Base(DeclarativeBase):
    pass


class AirQuality(Base):
    __tablename__ = "air_quality"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[d]
    city: Mapped[str] = mapped_column(String(100))
    pm25: Mapped[float]
    no2: Mapped[float]
    co2: Mapped[float]
    aqi: Mapped[float]
    level: Mapped[str] = mapped_column(String(50))


class Alerts(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[d] 
    city: Mapped[str] = mapped_column(String(100))
    aqi: Mapped [int]
   
def creat_tables(engine):
    Base.metadata.create_all(engine)