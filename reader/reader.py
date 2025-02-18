from smartcard.System import readers
<<<<<<< HEAD

from data_handler.config import retry_limit
from display.message import lookup
import sys
import time


def initialize_reader():
    global RETRY
    r = readers()
    if len(r) < 1:
        def loopcheck():
            global RETRY
            if RETRY < retry_limit:
                RETRY += 1
                lookup(1)
                time.sleep(5)
                loopcheck()
            else:
                sys.exit()

        loopcheck()
        return None
    else:
        return r[0]


def connect_reader(reader):
    print(f"[GENERAL] Reader Detected: {reader}")
    connection = reader.createConnection()
    connection.connect()
    return connection
=======
import time

def initialize_reader():
    """Initialize the NFC reader and return it."""
    r = readers()
    if len(r) < 1:
        print("[ERROR] No reader found. Please check your connection.")
        return None
    return r[0]

def monitor_card(reader):
    """Continuously check for card presence and establish a connection when detected."""
    print(f"[GENERAL] Monitoring Reader: {reader}")
    
    while True:
        try:
            connection = reader.createConnection()
            connection.connect()
            print("[SUCCESS] Card detected and connected.")
            return connection 
        except Exception:
            print("[INFO] No card detected. Waiting for a card...")
            time.sleep(1)  # Prevent excessive CPU usage

def wait_for_new_card(reader):
    """Waits for a new card after removal and re-establishes the connection."""
    print("[INFO] Card removed. Waiting for a new card...")

    while True:
        try:
            connection = reader.createConnection()
            connection.connect()
            print("[SUCCESS] New card detected and connected.")
            return connection  
        except Exception:
            print("[INFO] No card detected. Waiting...")
            time.sleep(1)  # Prevent excessive polling
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
