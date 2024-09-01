import json

# Load the JSON data from the file
file_path = 'data/english_llama_ref_data.json'
with open(file_path, 'r') as file:
    json_data = json.load(file)

# Print all attributes
def print_attributes(data, prefix=''):
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"{prefix}{key}")
            print_attributes(value, prefix + '  ')
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}[{i}]")
            print_attributes(item, prefix + '  ')

print_attributes(json_data)
