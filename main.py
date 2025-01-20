
from display.message import lookup
from reader.reader import initialize_reader, connect_reader
from reader.operations import detect_card_info, read_uid, read_sector, read_all_sectors
from data_handler.files import save_dump, load_dump, compare_card
from data_handler.write import write_card

import time


# Constants for Block Size
BLOCK_SIZE = 16
RETRY = 0

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
        print("[READ] 1. Load Decryption Keys.")
        print("[READ] 2. Print UID.")
        print("[READ] 3. Read All Sectors.")
        print("[READ] 4. Read Specific Sector.")
        print("[SAVE] 5. Dump Card.")
        print("[EXIT] 6. Exit.")
        print("[LOAD] 7. Load Dump.")
        print()  

        choice = input("Enter your choice: ")
        if choice == "1":
            print("Coming soon!")

        if choice == "2":
            read_uid(connection)
        elif choice == "3":
            all_sector_data = read_all_sectors(connection, num_sectors)
        elif choice == "4":
            sector = input("Enter sector: ")
            read_sector(connection, sector)
        elif choice == "5":
            filename = input("Enter filename: ")
            save_dump(all_sector_data, filename)
        elif choice == "6":
            print("[GENERAL] Exiting.")
            break
        elif choice == "7":
            dump_file = load_dump()
            if dump_file:
                while True:
                    print()
                    print("[CMPR] 8. Compare Loaded Dump to Current Card.")
                    print("[WRTE] 9. Write Loaded Dump to Current Card.")
                    print("[EXIT] 10. Back to Main Menu.")
                    print()
                    sub_choice = input("Enter your choice: ")
                    if sub_choice == "8":
                        compare_card(dump_file, connection, num_sectors)
                    elif sub_choice == "9":
                        write_card(dump_file, connection)
                    elif sub_choice == "10":
                        break