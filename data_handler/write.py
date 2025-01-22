
import json

def write_card(dump_file, connection):
    print("[WRITE] Writing dump data to the card...")
    
    with open(dump_file, 'r') as file:
        dump_data = json.load(file)

    for sector_str, blocks in dump_data.items():
        sector = int(sector_str)
        print(f"Writing to Sector {sector}")

       
        block_to_authenticate = sector * 4
        for key_type in [0x60, 0x61]:  
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

    print("[WRITE] Writing completed.")
