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

# Initialize lists to hold URLs and levels
urls = []
levels = []

with open('/Users/and_seb/Documents/Programming/Chinese Language Classifier/Web Scraping/Links for Scraping/YesChinese Links.txt', 'r') as file:
    lines = file.readlines()
    
    # Iterate over lines, reading a pair of lines at a time
    for i in range(0, len(lines), 2):
        url_line = lines[i].strip()  # URL line (removing newline characters and spaces)
        level_line = lines[i+1].strip()  # Level line
        
        # Add the URL and level to their respective lists
        urls.append(url_line)
        levels.append(level_line)


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

for url, level in zip(urls, levels):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Convert the entire page text to a string for searching
    page_text = soup.get_text()
    chinesetext = soup.find_all(class_="readplay_r2_r_artice")
    print(level)

    clean_chinesetext = ''
    for element in chinesetext:
        text = element.get_text().strip()
        clean_chinesetext += text
            # Check if any of the terms are in the current text block


    # Create a dictionary for storing the data
    data = {
        "text": clean_chinesetext,  # Use .strip() to remove leading/trailing whitespace
        "HSK_level": level,  # Assuming you have logic to set the HSK level
        "source_url": url,
        "retrieved_date": datetime.now().strftime('%d-%m-%Y')  # Gets the current date in the specified format
    }

    # Serialize the dictionary to a JSON string
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Define directory file path and ensure it exists
    dir_path = os.path.join("/Users/and_seb/Documents/Programming/Chinese Language Classifier/extracted_texts")
    os.makedirs(dir_path, exist_ok=True) # Ensure the directory exists

    # Get the next available file number for the new filename
    file_num = get_next_file_number(dir_path, level)
    filename = f"{level}_{file_num}.json"
    filepath = os.path.join(dir_path, filename)

    print(json_data)
    # Write the JSON string to a file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(json_data)

    time.sleep(10)  # Pauses the execution for 10 seconds
