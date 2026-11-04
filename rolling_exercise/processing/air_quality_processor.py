from processing.calculate_aqi import calculate_aqi
from logger import logger

def process_air_quality(valid_rows):

    for row in valid_rows:
      aqi, level =   calculate_aqi(row["PM2.5"], row["NO2"], row["CO2"])

      row["aqi"] = aqi
      row["level"] = level 
      logger.info(f"City: {row['city']}, Date: {row['date']}, "f"AQI: {aqi}, Level: {level}")
      
    return valid_rows