import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup

# Function to fetch S&P 500 companies and their details
def fetch_sp500_companies():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})

        companies = {}
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cols = row.find_all('td')
            if cols:  # Ensure the row has columns
                symbol = cols[0].text.strip()
                name = cols[1].text.strip()  # Company name
                sector = cols[3].text.strip()  # GICS Sector
                sub_industry = cols[4].text.strip()  # GICS Sub-Industry
                headquarters = cols[5].text.strip()  # Headquarters Location
                date_added = cols[6].text.strip()  # Date added
                cik = cols[7].text.strip()  # CIK
                founded = cols[8].text.strip() if len(cols) > 8 else "Not specified"  # Founded

                companies[name.lower()] = {
                    'symbol': symbol,
                    'security': name,
                    'sector': sector,
                    'sub_industry': sub_industry,
                    'headquarters': headquarters,
                    'date_added': date_added,
                    'cik': cik,
                    'founded': founded
                }

        return companies
    else:
        st.error(f"Error fetching data from Wikipedia: {response.status_code}")
        return {}

# Function to fetch stock data for a given ticker symbol and days back
def fetch_stock_data(ticker, days_back):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    # Fetch stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date, interval='1d')
    return stock_data