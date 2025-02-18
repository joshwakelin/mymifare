code = {
    1: "[ERROR] No reader has been detected. Retrying in 5 seconds..",
    2: "[ERROR] Failed to find reader. Please retry when a reader is connected.",
    3: "[ERROR] Failed to detect card type.",
    4: "[ERROR] Failed to detect card type."
}


def lookup(var):
    print(code[var])
