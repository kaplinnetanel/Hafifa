from concurrent.futures import ThreadPoolExecutor
import os 
import pandas as pd 
from dotenv import load_dotenv 
import yfinance as yf 
from itertools import repeat

load_dotenv()

def get_bitcoin_price(date,ticker):
    stock = yf.Ticker(ticker)

    start = pd.Timestamp(date).floor("h")
    end = start + pd.Timedelta(hours=1) 
    try:
        data = stock.history(
            start = start,
            end = end,
            interval = "1h"
        )
    except Exception as e:
        print(f"Eror:{e}")    
        return None
    
    if data.empty:
        return None
            
    open_price = data.iloc[0]["Open"]
    close_price = data.iloc[0]["Close"]

    change = (close_price - open_price ) / open_price * 100
    
    return change 
    
def read_dates(env_name):


    file_path = os.environ[env_name]
    dates = pd.read_csv(file_path, header=None)
    return pd.to_datetime(dates[0]).tolist()

def save_to_csv(all_data):
    file_path = os.environ["DESTINATION_FILE"]

    df = pd.concat(all_data, ignore_index= True)

    df.to_csv(file_path, index=False)
  
def run_stock(executor, env_name, ticker):
    dates = read_dates(env_name)
    results = list(executor.map(
        get_bitcoin_price,
        dates,
        repeat(ticker)
    ))
    return dates, results

def process_stocks():
    stocks = {
        "Bitcoin": ("BITCOIN_DATES", "BTC-USD"),
        "Amazon": ("AMAZON_DATES", "AMZN"),
        "Google": ("GOOGLE_DATES", "GOOGL")
    }

    all_data = []

    with ThreadPoolExecutor(max_workers=5) as executor:
        for stock_name, (env_name, ticker) in stocks.items():
            dates, results = run_stock(executor, env_name, ticker)
            print(stock_name)
            print("good:", sum(x is not None for x in results))
            print("not good:", sum(x is None for x in results))
            df = pd.DataFrame({
                "hour": dates,
                "stock type": stock_name,
                "percentage change": results
            })
            df = df.dropna(subset= ["percentage change"])
            all_data.append(df) 
        
    save_to_csv(all_data)



if __name__ == "__main__":
    process_stocks()






