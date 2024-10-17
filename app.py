import streamlit as st
import pandas as pd
import sqlite3
import time

# Set Streamlit layout and page title
st.set_page_config(page_title="RFID Data Viewer", layout="wide")

# Function to load data from SQLite database
def load_data():
    conn = sqlite3.connect('rfid_data.db')
    df = pd.read_sql_query("SELECT * FROM rfid_data", conn)
    conn.close()
    return df

# Load the CSS for custom styling
def load_css():
    st.markdown("""
    <style>
    /* Custom styles for the table */
    .css-18e3th9 {
        background-color: #2b2b2b;
    }
    .css-1d391kg {
        color: #e0e0e0;
    }
    .dataframe {
        width: 100%;
        background-color: #333333;
        color: #ffffff;
        border-collapse: collapse;
    }
    .dataframe th {
        background-color: #4CAF50;
        color: white;
        padding: 12px;
        text-align: left;
    }
    .dataframe td {
        background-color: #444444;
        padding: 10px;
        border: 1px solid #555555;
    }
    .dataframe tbody tr:nth-child(even) {
        background-color: #3a3a3a;
    }
    .dataframe tbody tr:hover {
        background-color: #555555;
    }
    .stDataFrame {
        height: 500px !important;
        overflow-y: auto;
        border: 1px solid #444444;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Streamlit App
def main():
    load_css()  # Load custom CSS
    st.title("RFID Data Viewer")
    st.subheader("Live RFID data from the database")

    # Create a placeholder for the data
    placeholder = st.empty()

    # Loop to refresh the data every 5 seconds
    while True:
        # Load data from SQLite database
        data = load_data()

        # Display data in a customized table
        with placeholder.container():  # Use the placeholder to update the table
            st.dataframe(data, height=500)  # Adjust height as needed

        # Pause for 5 seconds before reloading data
        time.sleep(5)

if __name__ == "__main__":
    main()
