import json
import os

# Path to the directory containing your JSON files
directory_path = '/Users/and_seb/Documents/Programming/Chinese Language Classifier/chinesereader_texts'

# Loop through each file in the directory
for filename in os.listdir(directory_path):
    if filename.endswith('.json'):  # Check if the file is a JSON file
        file_path = os.path.join(directory_path, filename)
        
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Remove unwanted text from the 'text' field
        unwanted_texts = ['\n',"Hide Pinyin", "Popup Chinese dictionary and Pinyin script created by Alex at Mandarinspot.com. Thank you Alex!"]
        for unwanted_text in unwanted_texts:
            if unwanted_text in data['text']:
                data['text'] = data['text'].replace(unwanted_text, '')

        # Write the modified JSON object back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
