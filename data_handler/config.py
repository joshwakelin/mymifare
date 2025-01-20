import json




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
