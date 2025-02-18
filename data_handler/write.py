<<<<<<< HEAD

import json

def write_card(dump_file, connection):
    print("[WRITE] Writing dump data to the card...")
    
    with open(dump_file, 'r') as file:
        dump_data = json.load(file)
=======
import json
import time

def write_card(dump_file, connection):
    """Writes the loaded dump data to the card, handling authentication and errors."""
    print("[WRITE] Writing dump data to the card...")

    try:
        with open(dump_file, 'r') as file:
            dump_data = json.load(file)
    except Exception as e:
        print(f"[ERROR] Failed to load dump file: {e}")
        return
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)

    for sector_str, blocks in dump_data.items():
        sector = int(sector_str)
        print(f"Writing to Sector {sector}")

<<<<<<< HEAD
       
        block_to_authenticate = sector * 4
        for key_type in [0x60, 0x61]:  
            COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, block_to_authenticate, key_type, 0x00]
            data, sw1, sw2 = connection.transmit(COMMAND)
            if (sw1, sw2) == (0x90, 0x00):
                print(f"Authenticated to Sector {sector} with Key {'A' if key_type == 0x60 else 'B'}.")
                break
        else:
            print(f"Authentication to Sector {sector} failed. Skipping this sector.")
=======
        block_to_authenticate = sector * 4
        authenticated = False

        for key_type in [0x60, 0x61]:  # Try Key A (0x60) first, then Key B (0x61)
            try:
                COMMAND = [0xFF, 0x86, 0x00, 0x00, 0x05, 0x01, 0x00, block_to_authenticate, key_type, 0x00]
                data, sw1, sw2 = connection.transmit(COMMAND)
                
                if (sw1, sw2) == (0x90, 0x00):
                    print(f"Authenticated to Sector {sector} with Key {'A' if key_type == 0x60 else 'B'}.")
                    authenticated = True
                    break
            except Exception as e:
                print(f"[ERROR] Authentication failed for Sector {sector}: {e}")
        
        if not authenticated:
            print(f"[WARNING] Authentication to Sector {sector} failed. Skipping this sector.")
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
            continue

        for block_str, block_data in blocks.items():
            block_num = int(block_str)
<<<<<<< HEAD
            block_data = bytes(block_data)  

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
=======
            block_data = bytes(block_data) 

            if len(block_data) != 16:
                print(f"[WARNING] Block {block_num} data is not 16 bytes. Skipping.")
                continue

            if block_num % 4 == 3:  
                print(f"[INFO] Skipping trailer block {block_num} in Sector {sector} to avoid overwriting keys.")
                continue

            try:
                COMMAND = [0xFF, 0xD6, 0x00, block_num, 0x10] + list(block_data)
                data, sw1, sw2 = connection.transmit(COMMAND)

                if (sw1, sw2) == (0x90, 0x00):
                    print(f"[SUCCESS] Wrote to Block {block_num} in Sector {sector}")
                else:
                    print(f"[ERROR] Failed to write to Block {block_num} in Sector {sector}. Status: {sw1:02X} {sw2:02X}")
            except Exception as e:
                print(f"[ERROR] Failed to write to Block {block_num} in Sector {sector}: {e}")
        
        time.sleep(0.1)  
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)

    print("[WRITE] Writing completed.")
