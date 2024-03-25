from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import re
import os
import time

# Set up the WebDriver
service = Service('/Users/and_seb/Documents/Programming/Chinese Language Classifier/chromedriver')
driver = webdriver.Chrome(service=service)

with open('Chinese Reader Links.txt', 'r') as file:
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

# urls = ['http://chinesereadingpractice.com/2011/12/20/my-familys-dragon-boat-festival/']

for url in urls:
    print(url)
    # Open a webpage
    try:
        driver.get(url)

        # Click the button to load content
        button = driver.find_element(By.CLASS_NAME, 'toggleButton')  # Replace 'button-id' with the actual button's ID
        ActionChains(driver).move_to_element(button).click(button).perform()

        # Wait for the 'rt' elements to load after clicking the button
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "rt"))
        )

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Convert the entire page text to a string for searching
        page_text = soup.get_text()
        chinesetext = soup.find_all(id="chinesetext")
        translation = soup.find_all(class_="hide-this-part")
        term = soup.find_all(rel="category tag")

        # Check if any of the terms are in the page text
        for element in term:
            text = element.get_text().strip()
            if "Beginner" in text:
                level =  "HSK3"
            elif "Intermediate" in text:
                level =  "HSK4"
            elif "Advanced" in text:
                level =  "HSK5"
            else:
                level = "Undefined"

        clean_chinesetext = ''
        clean_translation = ''
        pinyin = ''
        for element in chinesetext:
            text = element.get_text().strip()
            clean_chinesetext += text
        for element in translation:
            text = element.get_text().strip()
            clean_translation += text

        # Now that the 'rt' elements are loaded, you can get their text content
        rt_elements = driver.find_elements(By.TAG_NAME, 'rt')
        for element in rt_elements:
            pinyin += element.text
            pinyin += ' '

        # Create a dictionary for storing the data
        data = {
            "text": clean_chinesetext,  # Use .strip() to remove leading/trailing whitespace
            "translation": clean_translation,  # Use .strip() to remove leading/trailing whitespace,  # Use .strip() to remove leading/trailing whitespace
            "pinyin": pinyin,
            "HSK_level": level,  # Assuming you have logic to set the HSK level
            "source_url": url,
            "retrieved_date": datetime.now().strftime('%d-%m-%Y')  # Gets the current date in the specified format
        }

        # Serialize the dictionary to a JSON string
        json_data = json.dumps(data, ensure_ascii=False, indent=4)

        # Define directory file path and ensure it exists
        dir_path = os.path.join("/Users/and_seb/Documents/Programming/Chinese Language Classifier/chinesereader_texts")
        os.makedirs(dir_path, exist_ok=True) # Ensure the directory exists

        # Get the next available file number for the new filename
        file_num = get_next_file_number(dir_path, level)
        filename = f"{level}_{file_num}.json"
        filepath = os.path.join(dir_path, filename)

        # Write the JSON string to a file
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(json_data)
    
    except Exception as e:
        print(f"Error processing {url}: {e}")
        with open("failed_urls.txt", 'w', encoding='utf-8') as file:
            file.write(url)
            file.write("\n")
    finally:
        # Short delay between requests
        time.sleep(10)

# Clean up: close the browser window
driver.quit()
