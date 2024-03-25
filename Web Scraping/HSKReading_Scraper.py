import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

with open('HSK Reader Links.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Function to find the next available file number in the directory
def get_next_file_number(dir_path, level):
    # Create a regex pattern to match filenames and extract numbers
    pattern = re.compile(rf"{level}_(\d+).json")
    max_num = -1

    # List all files in the directory and find the highest number
    for filename in os.listdir(dir_path):
        match = pattern.match(filename)
        if match:
            num = int(match.group(1))  # The second group contains the number
            max_num = max(max_num, num)

    return max_num + 1  # Return the next available number

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    common_text = ["This website is completely free. If you have the means, please consider donating to help with maintenance costs. We appreciate your support!",
    "Practice your Mandarin reading.","Practice reading Chinese! Complete with Pinyin, English translations, comprehension questions and voice-overs."]


    # Convert the entire page text to a string for searching
    page_text = soup.get_text()

    # Terms to search for
    terms = ["HSK 1", "HSK 2", "HSK 3", "HSK 4", "HSK 5", "HSK 6"]

    # Check if any of the terms are in the page text
    for term in terms:
        if term in page_text:
            level = term

    level = level.replace(' ', '')

    p_elements = soup.find_all('p')

    extracted_text = ''
    for element in soup.find_all('p'):
        text = element.get_text().strip()
        if level in ["HSK1", "HSK2", "HSK3"] and text not in common_text:
            extracted_text += text
        elif level in ["HSK4"] and len(text) >= 10 and text not in common_text:
            extracted_text += text
        elif level in ["HSK5", "HSK6"] and len(text) >= 30 and text not in common_text:  # Check if the text has 20 or more characters
            extracted_text += text
            # Check if any of the terms are in the current text block


    # Create a dictionary for storing the data
    data = {
        "text": extracted_text,  # Use .strip() to remove leading/trailing whitespace
        "HSK_level": level,  # Assuming you have logic to set the HSK level
        "source_url": url,
        "retrieved_date": datetime.now().strftime('%d-%m-%Y')  # Gets the current date in the specified format
    }

    # Serialize the dictionary to a JSON string
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Define directory file path and ensure it exists
    dir_path = os.path.join("/Users/and_seb/Documents/Programming/Chinese Language Classifier/extracted_texts")
    os.makedirs(dir_path, exist_ok=True)  # Ensure the directory exists

    # Get the next available file number for the new filename
    file_num = get_next_file_number(dir_path, level)
    filename = f"{level}_{file_num}.json"
    filepath = os.path.join(dir_path, filename)

    # Write the JSON string to a file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json_data)

    time.sleep(10)  # Pauses the execution for 10 seconds
