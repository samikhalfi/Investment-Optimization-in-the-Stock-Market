import requests
import pandas as pd
import time
import os

API_KEY = 'cs3g1hhr01qkg08j9hcgcs3g1hhr01qkg08j9hd0'  

def fetch_company_news(symbol, from_date, to_date):
    url = f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={API_KEY}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  

        news_data = response.json()
        
        if news_data:
            news_df = pd.DataFrame(news_data)
            file_path = 'Data/Company_News.csv'
            news_df.to_csv(file_path, index=False)
            print(f"Fetched {len(news_data)} news articles for {symbol} from {from_date} to {to_date}.")
            return news_df
        else:
            print(f"No news found for {symbol} from {from_date} to {to_date}.")
            return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
if __name__ == "__main__":
    symbol = 'AAPL' 
    from_date = '2023-08-15'  
    to_date = '2024-08-20'

    fetch_company_news(symbol, from_date, to_date)
