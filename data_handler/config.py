import json
<<<<<<< HEAD




def load_config(file_path="config.json"):
    try:
        with open(file_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e: 
     
        return None

config = load_config()

if config:
    retry_limit = config.get("reader_retry_limit", 3)
    block_size = config.get("block_size", 16)
    save_directory = config.get("save_directory", "saves")
    print(f"Reader Retry Limit: {retry_limit}, Block Size: {block_size}, Save Directory: {save_directory}")
=======
import os

# Default configuration settings
DEFAULT_CONFIG = {
    "reader_retry_limit": 3,
    "block_size": 16,
    "save_directory": "saves"
}

CONFIG_FILE = "config.json"

def save_default_config(file_path=CONFIG_FILE):
    """Creates a default config file if one does not exist."""
    try:
        with open(file_path, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        print(f"[INFO] Default config file created at {file_path}")
    except Exception as e:
        print(f"[ERROR] Failed to create default config file: {e}")

def load_config(file_path=CONFIG_FILE):
    """Loads the configuration from a JSON file. If missing or invalid, it falls back to defaults and recreates the file."""
    if not os.path.exists(file_path):
        print(f"[WARNING] {file_path} not found. Creating a default config file.")
        save_default_config(file_path)
        return DEFAULT_CONFIG  # Return defaults immediately

    try:
        with open(file_path, "r") as f:
            config = json.load(f)

        # Ensure all required keys are present, and update the file if needed
        updated = False
        for key, value in DEFAULT_CONFIG.items():
            if key not in config:
                print(f"[WARNING] Missing '{key}' in {file_path}. Using default value: {value}")
                config[key] = value
                updated = True

        if updated:
            with open(file_path, "w") as f:
                json.dump(config, f, indent=4)
            print("[INFO] Missing values added to config file.")

        return config

    except (json.JSONDecodeError, IOError) as e:
        print(f"[ERROR] Failed to load {file_path}: {e}. Recreating the config file.")
        save_default_config(file_path)
        return DEFAULT_CONFIG

# Load the configuration
config = load_config()

# Extract settings safely
retry_limit = config.get("reader_retry_limit", DEFAULT_CONFIG["reader_retry_limit"])
block_size = config.get("block_size", DEFAULT_CONFIG["block_size"])
save_directory = config.get("save_directory", DEFAULT_CONFIG["save_directory"])

# Display loaded settings
print(f"[CONFIG] Reader Retry Limit: {retry_limit}, Block Size: {block_size}, Save Directory: {save_directory}")
>>>>>>> 5579bbc (Fixes #1 - Removed crash / program force-quitting on card remove/replace)
