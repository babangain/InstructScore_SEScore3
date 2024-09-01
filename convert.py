import json

# Define the instruction template
instruction_template = "You are evaluating English-to-Hindi Machine translation task."

# Read the JSONL file
input_file = 'Hin_train.jsonl.txt'
output_file = 'converted_Hin_train.json'

converted_data_list = []

with open(input_file, 'r', encoding='utf-8') as infile:
    for line in infile:
        data = json.loads(line)
        
        # Construct the input string
        input_text = (f'The correct translation is "{data["ref"]}". The model generated translation is "{data["translation"]}". '
                      'Please identify all errors within each model output, up to a maximum of five. For each error, please give me the '
                      'corresponding error type, major/minor label, error location of the model generated translation and explanation for the error. '
                      'Major errors can confuse or mislead the reader due to significant change in meaning, while minor errors don\'t lead to loss '
                      'of meaning but will be noticed.')
        
        # Construct the output string
        errors = []
        for completion in data["completion"]:
            error = {
                "error_type": completion["span_type"].replace('_', ' '),
                "major_minor": "Major" if completion["span_severity"] in ["Very High", "High"] else "Minor",
                "error_location": data["translation"][completion["span_start_offset"]:completion["span_end_offset"] + 1],
                "explanation": f'{completion["span_text"]} is incorrect in this context.'
            }
            errors.append(error)
        
        output_text = f'Your Translation contains {len(errors)} errors:\n'
        for i, error in enumerate(errors):
            output_text += (f'Error type {i+1}: {error["error_type"]}\n'
                            f'Major/minor: {error["major_minor"]}\n'
                            f'Error location {i+1}: "{error["error_location"]}"\n'
                            f'Explanation for error {i+1}: {error["explanation"]}\n')
        
        # Construct the final dictionary
        converted_data = {
            "instruction": instruction_template,
            "input": input_text,
            "output": output_text.strip()  # Remove trailing newline
        }
        
        # Add the converted data to the list
        converted_data_list.append(converted_data)

# Write the list of dictionaries to the output JSON file
with open(output_file, 'w', encoding='utf-8') as outfile:
    json.dump(converted_data_list, outfile, ensure_ascii=False, indent=4)
