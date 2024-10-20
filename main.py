from smartcard.System import readers
from smartcard.util import toHexString
from smartcard.ATR import ATR
import sys
import os
import time
import json

# Constants for Block Size
BLOCK_SIZE = 16
RETRY = 0

# ASCII art for the menu
def print_ascii_art():
    art = r"""
  ________________________________________________________________________________________________

    _____ ______       ___    ___      _____ ______   ___  ________ ________  ________  _______      
|\   _ \  _   \    |\  \  /  /|    |\   _ \  _   \|\  \|\  _____\\   __  \|\   __  \|\  ___ \     
\ \  \\\__\ \  \   \ \  \/  / /    \ \  \\\__\ \  \ \  \ \  \__/\ \  \|\  \ \  \|\  \ \   __/|    
 \ \  \\|__| \  \   \ \    / /      \ \  \\|__| \  \ \  \ \   __\\ \   __  \ \   _  _\ \  \_|/__  
  \ \  \    \ \  \   \/  /  /        \ \  \    \ \  \ \  \ \  \_| \ \  \ \  \ \  \\  \\ \  \_|\ \ 
   \ \__\    \ \__\__/  / /           \ \__\    \ \__\ \__\ \__\   \ \__\ \__\ \__\\ _\\ \_______\
    \|__|     \|__|\___/ /             \|__|     \|__|\|__|\|__|    \|__|\|__|\|__|\|__|\|_______|
                  \|___|/                                                                         

   ________________________________________________________________________________________________
    """
    print(art)


# Detect card type and number of sectors
def detect_card_info(connection):
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
        print("Unknown card type. Defaulting to 0 sectors.")
        return 0, cardname

    return num_sectors, cardname


# Initialize the card readers
def initialize_reader():
    global RETRY
    r = readers()
    if len(r) < 1:
        def loopcheck():
            global RETRY
            if RETRY < 3:
                RETRY += 1
                print("[ERROR] No reader has been detected. Retrying in 5 seconds..")
                time.sleep(5)
                loopcheck()
            else:
                print("[ERROR] Failed to find reader. Please retry when a reader is connected.")
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


# Read UID of the card
def read_uid(connection):
    COMMAND = [0xFF, 0xCA, 0x00, 0x00, 0x00]
    data, sw1, sw2 = connection.transmit(COMMAND)
    print("UID: " + toHexString(data))
    print("Status words: %02X %02X" % (sw1, sw2))


# Read a specific sector
def read_sector(connection, sector):
    COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, int(sector) * 4, 0x60, 0x00]
    data, sw1, sw2 = connection.transmit(COMMAND)

    if (sw1, sw2) == (0x90, 0x0):
        print(f"Status: Decryption sector {sector} using Key A successful.")
    elif (sw1, sw2) == (0x63, 0x0):
        print(f"Status: Decryption sector {sector} failed. Trying as Key B.")
        COMMAND[8] = 0x61
        data, sw1, sw2 = connection.transmit(COMMAND)
        if (sw1, sw2) == (0x90, 0x0):
            print(f"Status: Decryption sector {sector} using Key B successful.")
        else:
            print(f"Status: Decryption sector {sector} failed.")
            return None

    sector_data = {}
    print(f"Sector {sector}")
    for block in range(int(sector) * 4, int(sector) * 4 + 4):
        COMMAND = [0xFF, 0xB0, 0x00, block, BLOCK_SIZE]
        data, sw1, sw2 = connection.transmit(COMMAND)
        print(
            f"Block {block}: "
            + toHexString(data)
            + " | "
            + "".join(chr(i) for i in data if 32 <= i <= 126)
        )
        sector_data[block] = data
    return sector_data


# Read all sectors
def read_all_sectors(connection, num_sectors):
    all_sector_data = {}
    print("[READ] Reading All Sectors:")
    for sector in range(num_sectors):
        sector_data = read_sector(connection, sector)
        if sector_data:
            all_sector_data[sector] = sector_data
    print("Completed reading all sectors.")
    return all_sector_data


# Save dump file
def save_dump(sector_data, filename):
    if not sector_data:
        print("[ERROR] No sector data available to save.")
        return

    file_path = os.path.join("saves", filename) + ".json"
    
    # Convert bytes to lists for JSON serialization
    json_data = {}
    for sector, blocks in sector_data.items():
        json_data[str(sector)] = {str(block): list(data) for block, data in blocks.items()}

    with open(file_path, "w") as dump_file:
        json.dump(json_data, dump_file, indent=2)
    
    print(f"Data saved to {file_path}")


# Load dump file
def load_dump():
    filename = input("Enter the load file name (without extension): ") + ".json"
    file_path = os.path.join("saves", filename)

    if not os.path.exists(file_path):
        print("File not found. Exiting.")
        return None

    print("File loaded successfully.")
    return file_path


# Compare card with loaded dump
def compare_card(dump_file, connection, num_sectors):
    current_card_data = read_all_sectors(connection, num_sectors)

    # Reading the dump file content
    with open(dump_file, 'r') as file:
        dump_data = json.load(file)

    differences = []

    # Compare sector by sector, block by block
    for sector_str, blocks in dump_data.items():
        sector = int(sector_str)
        if sector not in current_card_data:
            differences.append(f"Sector {sector} is missing in the current card.")
            continue

        for block_str, dump_block_data in blocks.items():
            block_num = int(block_str)
            current_block_data = list(current_card_data[sector][block_num])

            if current_block_data != dump_block_data:
                differences.append(f"Difference found in Sector {sector}, Block {block_num}:")
                differences.append(f"  Current: {current_block_data}")
                differences.append(f"  Dump: {dump_block_data}")

    # Output differences or indicate no differences found
    if not differences:
        print("No differences found between the card and the loaded dump.")
    else:
        for diff in differences:
            print(diff)


def write_card(dump_file, connection):
    print("[WRTE] Writing dump data to the card...")
    
    # Load dump data from JSON file
    with open(dump_file, 'r') as file:
        dump_data = json.load(file)

    for sector_str, blocks in dump_data.items():
        sector = int(sector_str)
        print(f"Writing to Sector {sector}")

        # Authenticate to the sector before writing
        block_to_authenticate = sector * 4
        for key_type in [0x60, 0x61]:  # Try both Key A (0x60) and Key B (0x61)
            COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, block_to_authenticate, key_type, 0x00]
            data, sw1, sw2 = connection.transmit(COMMAND)
            if (sw1, sw2) == (0x90, 0x00):
                print(f"Authenticated to Sector {sector} with Key {'A' if key_type == 0x60 else 'B'}.")
                break
        else:
            print(f"Authentication to Sector {sector} failed. Skipping this sector.")
            continue

        for block_str, block_data in blocks.items():
            block_num = int(block_str)
            block_data = bytes(block_data)  # Convert list back to bytes

            if len(block_data) != 16:
                print(f"Block {block_num} data is not 16 bytes. Skipping.")
                continue

            if block_num % 4 == 3:
                print(f"Skipping trailer block {block_num} in Sector {sector} to avoid overwriting keys.")
                continue

            COMMAND = [0xFF, 0xD6, 0x00, block_num, 0x10] + list(block_data)
            data, sw1, sw2 = connection.transmit(COMMAND)
            if (sw1, sw2) == (0x90, 0x00):
                print(f"Successfully wrote to Block {block_num} in Sector {sector}")
            else:
                print(f"Failed to write to Block {block_num} in Sector {sector}. Status: {sw1:02X} {sw2:02X}")

    print("[WRTE] Writing completed.")


# Main interaction loop
print_ascii_art()
time.sleep(2)

reader = initialize_reader()
if reader:
    connection = connect_reader(reader)
    num_sectors, cardname = detect_card_info(connection)
    time.sleep(2)

    dump_file = None

    while True:
        print()  
        print("Choose a menu option.")
        print()  
        print("[READ] 1. Print UID.")
        print("[READ] 2. Read All Sectors.")
        print("[READ] 3. Read Specific Sector.")
        print("[SAVE] 4. Dump Card.")
        print("[EXIT] 5. Exit.")
        print("[LOAD] 6. Load Dump.")
        print()  

        choice = input("Enter your choice: ")
        if choice == "1":
            read_uid(connection)
        elif choice == "2":
            all_sector_data = read_all_sectors(connection, num_sectors)
        elif choice == "3":
            sector = input("Enter sector: ")
            read_sector(connection, sector)
        elif choice == "4":
            filename = input("Enter filename: ")
            save_dump(all_sector_data, filename)
        elif choice == "5":
            print("[GENERAL] Exiting.")
            break
        elif choice == "6":
            dump_file = load_dump()
            if dump_file:
                while True:
                    print()
                    print("[CMPR] 7. Compare Loaded Dump to Current Card.")
                    print("[WRTE] 8. Write Loaded Dump to Current Card.")
                    print("[EXIT] 9. Back to Main Menu.")
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "7":
                        compare_card(dump_file, connection, num_sectors)
                    elif sub_choice == "8":
                        write_card(dump_file, connection)
                    elif sub_choice == "9":
                        break