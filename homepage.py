import streamlit as st
from UI.pages.page_data import display_data_page
from UI.pages.page_vizual import display_stock_dashboard

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data", "Visualization"])

# Call the appropriate function based on the selected page
if page == "Data":
    display_data_page()

elif page == "Visualization":
    display_stock_dashboard()
    # Add visualizations logic here, e.g., st.line_chart(your_dataframe['Close Price'])
