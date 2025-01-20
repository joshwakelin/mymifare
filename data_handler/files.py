import os
import json


from reader.operations import read_all_sectors

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


def load_dump():
    filename = input("Enter the load file name (without extension): ") + ".json"
    file_path = os.path.join("saves", filename)

    if not os.path.exists(file_path):
        print("File not found. Exiting.")
        return None

    print("File loaded successfully.")
    return file_path


def compare_card(dump_file, connection, num_sectors):
    current_card_data = read_all_sectors(connection, num_sectors)


    with open(dump_file, 'r') as file:
        dump_data = json.load(file)

    differences = []


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