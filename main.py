<<<<<<< HEAD

from display.message import lookup
from reader.reader import initialize_reader, connect_reader
=======
from reader.reader import initialize_reader, monitor_card, wait_for_new_card
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
from reader.operations import detect_card_info, read_uid, read_sector, read_all_sectors
from data_handler.files import save_dump, load_dump, compare_card
from data_handler.write import write_card

import time

<<<<<<< HEAD

# Constants for Block Size
BLOCK_SIZE = 16
RETRY = 0

=======
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
print(r"""
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
<<<<<<< HEAD
    """)




# Main interaction loop
time.sleep(2)

reader = initialize_reader()
if reader:
    connection = connect_reader(reader)
    num_sectors, cardname = detect_card_info(connection)
    

    dump_file = None
    time.sleep(2)
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
                    print()
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "7":
                        compare_card(dump_file, connection, num_sectors)
                    elif sub_choice == "8":
                        write_card(dump_file, connection)
                    elif sub_choice == "9":
                        break
=======
""")

time.sleep(2)

reader = initialize_reader()
if not reader:
    print("[ERROR] No reader detected. Exiting program.")
    exit()

connection = monitor_card(reader)

num_sectors, cardname = detect_card_info(connection)
time.sleep(2)

while True:
    print("\nChoose a menu option.\n")
    print("[READ] 1. Print UID.")
    print("[READ] 2. Read All Sectors.")
    print("[READ] 3. Read Specific Sector.")
    print("[SAVE] 4. Dump Card.")
    print("[EXIT] 5. Exit.")
    print("[LOAD] 6. Load Dump.\n")

    choice = input("Enter your choice: ")

    if choice == "1":
        while True:
            try:
                read_uid(connection)
                break
            except Exception:
                print("[INFO] No card detected. Waiting for a new card...")
                connection = wait_for_new_card(reader)

    elif choice == "2":
        while True:
            try:
                all_sector_data = read_all_sectors(connection, num_sectors)
                break
            except Exception:
                print("[INFO] No card detected. Waiting for a new card...")
                connection = wait_for_new_card(reader)

    elif choice == "3":
        sector = input("Enter sector: ")
        while True:
            try:
                read_sector(connection, sector)
                break
            except Exception:
                print("[INFO] No card detected. Waiting for a new card...")
                connection = wait_for_new_card(reader)

    elif choice == "4":
        filename = input("Enter filename: ")
        while True:
            try:
                save_dump(all_sector_data, filename)
                break
            except Exception:
                print("[INFO] No card detected. Waiting for a new card...")
                connection = wait_for_new_card(reader)

    elif choice == "5":
        print("[GENERAL] Exiting.")
        break

    elif choice == "6":
        dump_file = load_dump()
        if dump_file:
            while True:
                print("\n[CMPR] 7. Compare Loaded Dump to Current Card.")
                print("[WRTE] 8. Write Loaded Dump to Current Card.")
                print("[EXIT] 9. Back to Main Menu.\n")
                sub_choice = input("Enter your choice: ")
                if sub_choice == "7":
                    while True:
                        try:
                            compare_card(dump_file, connection, num_sectors)
                            break
                        except Exception:
                            print("[INFO] No card detected. Waiting for a new card...")
                            connection = wait_for_new_card(reader)
                
                elif sub_choice == "8":
                    while True:
                        try:
                            write_card(dump_file, connection)
                            break
                        except Exception:
                            print("[INFO] No card detected. Waiting for a new card...")
                            connection = wait_for_new_card(reader)

                elif sub_choice == "9":
                    break
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
