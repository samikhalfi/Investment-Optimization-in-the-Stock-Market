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

# Main function to display the Streamlit app
def display_data_page():
    st.title("Stock Market Data")

    # Fetch S&P 500 companies and store in session state
    if 'companies' not in st.session_state:
        st.session_state.companies = fetch_sp500_companies()

    # Input for the company name
    company_input = st.text_input("Enter part of the company name (e.g., Apple):", "").strip().lower()

    if company_input:  # Proceed only if there's input
        # Filter companies based on user input
        filtered_companies = {name: details for name, details in st.session_state.companies.items() if company_input in name}

        if filtered_companies:
            # Display matching company details
            st.write(f"### Matching Companies for '{company_input}':")
            for name, details in filtered_companies.items():
                if isinstance(details, dict):  # Check if details is a dictionary
                    st.write(f"**Company:** {details['security']} - **Symbol:** {details['symbol']}")
                else:
                    st.error(f"Expected a dictionary for {name}, but got {type(details)}")  # Error handling
            
            # Select one of the filtered companies to display more data
            selected_company = st.selectbox("Select a company for more details:", list(filtered_companies.keys()))
            selected_details = filtered_companies[selected_company]

            # Store the selected company's security name in session state
            st.session_state['selected_security'] = selected_details['security']

            # Show detailed information for the selected company
            st.write(f"### Details for {selected_details['security']}:")
            st.write(f"**Symbol:** {selected_details['symbol']}")
            st.write(f"**Sector:** {selected_details['sector']}")
            st.write(f"**Sub-Industry:** {selected_details['sub_industry']}")
            st.write(f"**Headquarters:** {selected_details['headquarters']}")
            st.write(f"**Date Added:** {selected_details['date_added']}")
            st.write(f"**CIK:** {selected_details['cik']}")
            st.write(f"**Founded:** {selected_details['founded']}")

            # Show the selected symbol
            st.success(f"The symbol for {selected_company.capitalize()} is **{selected_details['symbol']}**.")

            # Date picker and slider
            st.subheader("Select Date Range for Stock Data")
            days_slider = st.slider("Select number of days back from today:", min_value=1, max_value=30, value=30)

            # Fetch stock data
            stock_data = fetch_stock_data(selected_details['symbol'], days_slider)

            if not stock_data.empty:
                st.write(f"Showing stock data for {selected_details['security']} ({selected_details['symbol']}) for the last {days_slider} days.")
                st.dataframe(stock_data)

                # Save the CSV file to the Data directory
                csv_file_path = 'Data/historical_data.csv'
                stock_data.to_csv(csv_file_path, index=True)  # Save stock data to CSV in the Data directory

                # Provide a download button for the saved CSV file
                with open(csv_file_path, 'r') as file:
                    csv_data = file.read()  # Read the file content

                st.download_button(
                    label="Download Historical Data",
                    data=csv_data,
                    file_name=f"{selected_details['security']}_historical_data.csv",
                    mime="text/csv"
                )
            else:
                st.error("No historical stock data available for this company in the selected date range.")
        else:
            st.warning("No companies found matching your input. Please try again.")
    else:
        st.info("Please enter a company name to see the details.")

# Call the display function
if __name__ == "__main__":
    display_data_page()
