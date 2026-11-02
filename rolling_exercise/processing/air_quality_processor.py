from calculate_aqi import calculate_aqi

def process_air_quality(valid_rows):

    for row in valid_rows:
      aqi, level =   calculate_aqi(row["PM2.5"], row["NO2"], row["CO2"])

      row["aqi"] = aqi
      row["level"] = level 
      
    return valid_rows