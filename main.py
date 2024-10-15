import streamlit as st
from UI.pages.page_data import display_data_page
from UI.pages.page_vizual import display_stock_dashboard

# Set the page configuration
st.set_page_config(page_title="Investment Dashboard", layout="wide")

# Display a header with an icon and a PNG image using st.image
st.image('assets/logo.png', caption='Stock Trader Prophet', width=200)



# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data", "Visualization"])

# Call the appropriate function based on the selected page
if page == "Data":
    display_data_page()

elif page == "Visualization":
    display_stock_dashboard()
