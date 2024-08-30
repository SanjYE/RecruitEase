import os
import json
import openai


openai.api_key = '***'    #hidden for security reasons

def read_text_file(file_path):
    encodings = ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Unable to read the file {file_path} with any of the attempted encodings.")

def process_text_with_openai(text):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that processes placement criteria and converts it to a structured JSON format."},
            {"role": "user", "content": f"Convert the following placement criteria text to JSON format:\n\n{text}\n\nUse the following structure:\n{{\"companies\": [{{\"name\": \"Company Name\", \"role\": \"Job Role\", \"criteria\": {{\"minimum_gpa\": float, \"year_of_study\": \"string\", \"major\": \"string\", \"skills\": [\"skill1\", \"skill2\"], \"projects\": \"string\"}}}}]}}"}
        ]
    )
    content = response.choices[0].message.content
    print("API Response:", content)  
    return content

def validate_json(data):
    try:
        json_object = json.loads(data)
        return json_object
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        print("Received data:", data)
        return None

def save_json_file(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

def main():
    input_file = 'placements_part_4.txt'  
    output_file = 'placement_criteria_4.json'

    try:
       
        input_text = read_text_file(input_file)
        print(f"Input text (first 100 characters): {input_text[:100]}...")  # Debug print

        
        json_data = process_text_with_openai(input_text)

        
        parsed_data = validate_json(json_data)
        if parsed_data is None:
            raise ValueError("Failed to parse the API response as JSON")

        
        save_json_file(parsed_data, output_file)

        print(f"Processed data has been saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()