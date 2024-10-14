import streamlit as st
from UI.pages.page_data import display_data_page

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data", "Visualization"])

# Call the appropriate function based on the selected page
if page == "Data":
    display_data_page()

elif page == "Visualization":
    st.title("Visualization")
    st.write("This page will contain the visualizations.")
    # Add visualizations logic here, e.g., st.line_chart(your_dataframe['Close Price'])
