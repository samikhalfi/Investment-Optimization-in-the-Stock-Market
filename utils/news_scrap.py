import requests
import pandas as pd
import time

API_KEY = 'cs4p4u1r01qgd1p6742gcs4p4u1r01qgd1p67430'

def fetch_company_news(symbol, from_date, to_date):
    url = f'https://finnhub.io/api/v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()

        news_data = response.json()
        
        news_df = pd.DataFrame(news_data)
        
        if 'datetime' in news_df.columns:

            news_df['date'] = pd.to_datetime(news_df['datetime'], unit='s').dt.date
        
        news_df = news_df[['headline', 'date', 'url']]

        csv_filename = f'Data/Company_News.csv'
        news_df.to_csv(csv_filename, index=False)

        print(f"Fetched {len(news_data)} news articles for {symbol} from {from_date} to {to_date}.")
        return news_df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    symbol = 'AAPL'
    from_date = '2023-08-15'
    to_date = '2024-08-20'

    fetch_company_news(symbol, from_date, to_date)
