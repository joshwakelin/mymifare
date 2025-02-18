import os
import json
from reader.operations import read_all_sectors
from reader.reader import wait_for_new_card

def save_dump(sector_data, filename):
    """Saves sector data to a JSON file, ensuring proper serialization and directory handling."""
    if not sector_data:
        print("[ERROR] No sector data available to save.")
        return

    try:
        if not os.path.exists("saves"):
            os.makedirs("saves")

        file_path = os.path.join("saves", filename) + ".json"

        json_data = {}
        for sector, blocks in sector_data.items():
            json_data[str(sector)] = {str(block): list(data) for block, data in blocks.items()}

        with open(file_path, "w") as dump_file:
            json.dump(json_data, dump_file, indent=2)

        print(f"[SUCCESS] Data saved to {file_path}")

    except Exception as e:
        print(f"[ERROR] Failed to save dump: {e}")

def load_dump():
    """Loads a dump file and ensures it exists before returning the file path."""
    filename = input("Enter the load file name (without extension): ") + ".json"
    file_path = os.path.join("saves", filename)

    if not os.path.exists(file_path):
        print("[ERROR] File not found. Please check the filename and try again.")
        return None

    print("[SUCCESS] File loaded successfully.")
    return file_path

def compare_card(dump_file, connection, num_sectors):
    """Compares the current card's data with a saved dump file, with reconnection handling."""
    try:
        while True:
            try:
                print("[COMPARE] Reading current card data...")
                current_card_data = read_all_sectors(connection, num_sectors)
                break
            except Exception:
                print("[INFO] Card removed. Waiting for a new card...")
                connection = wait_for_new_card(connection)

        with open(dump_file, 'r') as file:
            dump_data = json.load(file)

        differences = []

        for sector_str, blocks in dump_data.items():
            sector = int(sector_str)
            if sector not in current_card_data:
                differences.append(f"[DIFFERENCE] Sector {sector} is missing in the current card.")
                continue

            for block_str, dump_block_data in blocks.items():
                block_num = int(block_str)
                
                if sector not in current_card_data or block_num not in current_card_data[sector]:
                    differences.append(f"[DIFFERENCE] Sector {sector}, Block {block_num} is missing.")
                    continue

                current_block_data = list(current_card_data[sector][block_num])

                if current_block_data != dump_block_data:
                    differences.append(f"[DIFFERENCE] Sector {sector}, Block {block_num}:")
                    differences.append(f"  Current: {current_block_data}")
                    differences.append(f"  Dump: {dump_block_data}")

        if not differences:
            print("[SUCCESS] No differences found between the card and the loaded dump.")
        else:
            for diff in differences:
                print(diff)

    except Exception as e:
        print(f"[ERROR] Failed to compare card data: {e}")
