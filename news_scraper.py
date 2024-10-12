import requests
import pandas as pd
import time


API_KEY = 'cs3g1hhr01qkg08j9hcgcs3g1hhr01qkg08j9hd0'  
def fetch_company_news(symbol, from_date, to_date):
    url = f'    /v1/company-news?symbol={symbol}&from={from_date}&to={to_date}&token={API_KEY}'

    try:

        response = requests.get(url)
        response.raise_for_status()  

        news_data = response.json()
        
        news_df = pd.DataFrame(news_data)

        news_df.to_csv(f'{symbol}_company_news_{from_date}_to_{to_date}.csv', index=False)

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
