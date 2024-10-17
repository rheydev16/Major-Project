import threading
import serial
import sqlite3
import time
from datetime import datetime
import streamlit as st
import pandas as pd
import subprocess

# RFID Script Function
def rfid_reader():
    # Set up serial communication (adjust 'COM9' for your actual port)
    ser = serial.Serial('COM6', 9600, timeout=1)
    time.sleep(2)  # Wait for serial connection to establish

    # Set up SQLite database connection
    conn = sqlite3.connect('rfid_data.db')
    cursor = conn.cursor()

    # Create a table to store RFID data if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rfid_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rfid_uid TEXT NOT NULL,
        timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
    )
    ''')
    conn.commit()

    def store_rfid_data(uid):
        # Insert RFID UID into the database along with the current timestamp
        local_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO rfid_data (rfid_uid, timestamp) VALUES (?, ?)', (uid, local_time))
        conn.commit()

    # Continuously read RFID
    while True:
        if ser.in_waiting > 0:
            # Read the RFID UID from the serial connection
            rfid_uid = ser.readline().decode('utf-8').strip()
            if rfid_uid:
                print(f"RFID UID: {rfid_uid}")
                store_rfid_data(rfid_uid)
        time.sleep(1)

    # Close the SQLite connection and serial port when done (though loop never ends)
    conn.close()
    ser.close()

# Streamlit Web App Function
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

# Main function to run both threads
def main():
    # Create threads for RFID reader and Streamlit
    rfid_thread = threading.Thread(target=rfid_reader)
    streamlit_thread = threading.Thread(target=run_streamlit)

    # Start both threads
    rfid_thread.start()
    streamlit_thread.start()

    # Keep the main thread alive while the other threads are running
    rfid_thread.join()
    streamlit_thread.join()

if __name__ == "__main__":
    main()
