JSON_FILE = "./dataset/data.json"

import json
import os
from datetime import datetime

def append_to_json_file(file_path, new_data):
    try:
        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)  # Load the existing data
        else:
            # If file is empty or doesn't exist, initialize with an empty list
            data = []

        # Ensure that new_data is a list of JSON objects
        if isinstance(new_data, list):
            # Process each item in new_data
            for item in new_data:
                # Add a 'date' field to each entry
                item['date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Remove 'score' and 'raw_content' fields if they exist
                item.pop('score', None)
                item.pop('raw_content', None)

            # Concatenate the new data to the existing data
            data.extend(new_data)

        # Write the updated data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("Data appended successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

def append_string_to_json_file(file_path, new_string):
    try:
        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Prepare the string entry as a dictionary
        entry = {
            'content': new_string,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        # Append the entry
        data.append(entry)

        # Write back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print("String appended successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        
def json_file_to_string(file_path):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Convert the loaded data into a JSON string
        json_string = json.dumps(data, indent=4)  # The indent is optional but formats the string neatly

        return json_string

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def clear_json_file(file_path):
    """
    This function clears the contents of the specified JSON file.
    """
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            with open(file_path, 'w') as file:
                file.truncate(0)  # Truncate the file (this will empty the content)
            print("File cleared successfully!")
        else:
            print("File does not exist.")
    except Exception as e:
        print(f"An error occurred while clearing the file: {e}")
