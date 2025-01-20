from smartcard.System import readers

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


# Connect to the card reader
def connect_reader(reader):
    print(f"[GENERAL] Reader Detected: {reader}")
    connection = reader.createConnection()
    connection.connect()
    return connection
