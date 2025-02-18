from smartcard.util import toHexString
from smartcard.ATR import ATR
from data_handler.config import block_size
from display.message import lookup

def detect_card_info(connection):
    try:
        atr = ATR(connection.getATR())
        hb = toHexString(atr.getHistoricalBytes())
        cardname = hb[-17:-12]

        card_sector_map = {
            "00 01": 16,  
            "00 02": 40,  
            "00 03": 12,  
            "00 26": 10,  
            "F0 04": 16,  
            "F0 11": 16,  
            "F0 12": 32,  
        }

        num_sectors = card_sector_map.get(cardname, None)
        if num_sectors is None:
            lookup(3)
            return 0, cardname

        return num_sectors, cardname

    except Exception as e:
        print(f"[ERROR] Failed to detect card: {e}")
        return 0, None  

def read_uid(connection):
    COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    try:
        data, sw1, sw2 = connection.transmit(COMMAND)
        print("UID: " + toHexString(data))
        print("Status words: %02X %02X" % (sw1, sw2))
    except Exception as e:
        print(f"[ERROR] Failed to read UID: {e}")
        raise  

def read_sector(connection, sector):
    """Reads a specific sector from the card."""
    try:
        sector = int(sector)  
        COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, sector * 4, 0x60, 0x00]
        data, sw1, sw2 = connection.transmit(COMMAND)

        if (sw1, sw2) == (0x90, 0x00):
            print(f"Status: Decryption sector {sector} using Key A successful.")
        elif (sw1, sw2) == (0x63, 0x00):
            print(f"Status: Decryption sector {sector} failed. Trying as Key B.")
            COMMAND[8] = 0x61
            data, sw1, sw2 = connection.transmit(COMMAND)
            if (sw1, sw2) == (0x90, 0x00):
                print(f"Status: Decryption sector {sector} using Key B successful.")
            else:
                print(f"Status: Decryption sector {sector} failed.")
                return None

        sector_data = {}
        print(f"Sector {sector}")
        for block in range(sector * 4, sector * 4 + 4):
            COMMAND = [0xFF, 0xB0, 0x00, block, block_size]
            data, sw1, sw2 = connection.transmit(COMMAND)
            print(
                f"Block {block}: "
                + toHexString(data)
                + " | "
                + "".join(chr(i) for i in data if 32 <= i <= 126)
            )
            sector_data[block] = data
        return sector_data

    except Exception as e:
        print(f"[ERROR] Failed to read sector {sector}: {e}")
        raise  

def read_all_sectors(connection, num_sectors):
    """Reads all sectors of the card and handles disconnection issues."""
    all_sector_data = {}
    print("[READ] Reading All Sectors:")

    for sector in range(num_sectors):
        try:
            sector_data = read_sector(connection, sector)
            if sector_data:
                all_sector_data[sector] = sector_data
            else:
                print(f"[WARNING] Skipping sector {sector} due to read error.")
        except Exception as e:
            print(f"[ERROR] Card disconnected while reading sector {sector}: {e}")
            raise  

    print("Completed reading all sectors.")
    return all_sector_data
