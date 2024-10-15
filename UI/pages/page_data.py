import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from utils.informations import *

# Main function to display the Streamlit app
def display_data_page():
    st.title("📈 **Investor's Hub: Stock Market Data**")
    st.divider()
    
    # Fetch S&P 500 companies and store in session state
    if 'companies' not in st.session_state:
        st.session_state.companies = fetch_sp500_companies()



    company_input = st.text_input("🔎 Search for a Company Enter part of the company name (e.g., Apple)", "").strip().lower()

    st.divider()
    if company_input:  # Proceed only if there's input
        # Filter companies based on user input
        filtered_companies = {name: details for name, details in st.session_state.companies.items() if company_input in name}

        if filtered_companies:
            # Display matching company details
            st.subheader(" Matching Companies")
            st.write(f"Results for '{company_input}'")

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
            st.divider()
            st.subheader("📊 Company Details")
            st.write(f"**Symbol:** {selected_details['symbol']}")
            st.write(f"**Sector:** {selected_details['sector']}")
            st.write(f"**Sub-Industry:** {selected_details['sub_industry']}")
            st.write(f"**Headquarters:** {selected_details['headquarters']}")
            st.write(f"**Date Added:** {selected_details['date_added']}")
            st.write(f"**CIK:** {selected_details['cik']}")
            st.write(f"**Founded:** {selected_details['founded']}")

            st.success(f"Selected company: **{selected_details['security']}** - **{selected_details['symbol']}**")

            # Date picker and slider
            st.divider()
            st.subheader("📅 Select Date Range for Stock Data")
            days_slider = st.slider("Select number of days back from today:", min_value=1, max_value=30, value=30)

            # Fetch stock data
            stock_data = fetch_stock_data(selected_details['symbol'], days_slider)

            if not stock_data.empty:
                st.write(f"Displaying stock data for {selected_details['security']} ({selected_details['symbol']}) over the last {days_slider} days.")
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
