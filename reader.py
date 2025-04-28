# read json from file

import json
import os

def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data
    else:
        print("File not found: ", file_path)
        return None
    
if __name__ == "__main__":
    # read json from file
    data = read_json("591.json")
    if data:
        print("Data: ", data)
    else:
        print("No data found.")