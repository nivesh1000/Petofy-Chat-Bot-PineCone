import os
import json
from pathmaker import data_path

dataset_path = data_path()


def load_json():
    combined_data = []
    folder_path = dataset_path
    # Traverse through the directory tree using os.walk
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(".json"):
                file_path = os.path.join(root, filename)
                with open(file_path, "r") as f:
                    # Load JSON data from the file
                    data = json.load(f)
                    # Append to the combined list
                    combined_data.extend(data)

    return combined_data




load_json()
