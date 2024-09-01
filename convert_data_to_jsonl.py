import json
from tqdm import tqdm

def process_file(file_path, instruction_text, output_file_suffix):
    # Load the JSON data from the file
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Prepare the data
    new_data = []

    for item in tqdm(json_data['instances']):
        if 'input' in item and 'output' in item:
            # Remove the instruction from the input and create a separate key for it
            input_text = item['input'].replace(instruction_text, '').strip()
            new_entry = {
                'instruction': instruction_text,
                'input': input_text,
                'output': item['output']
            }
            new_data.append(new_entry)

    # Append "modified" to the output file name
    output_file_path = file_path.replace('.json', f'_{output_file_suffix}.json')

    # Write the data to a JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(new_data, output_file, indent=4)

    print(f"Data successfully written to {output_file_path}")

# Define the file paths and their respective replacement strings
files_and_instructions = [
    ('data/english_llama_ref_data.json', "You are evaluating Chinese-to-English Machine translation task."),
    ('data/german_llama_ref_data.json', "You are evaluating English-to-German Machine translation task.")
]

output_file_suffix = 'modified'

# Process each file
for file_path, instruction_text in files_and_instructions:
    process_file(file_path, instruction_text, output_file_suffix)
