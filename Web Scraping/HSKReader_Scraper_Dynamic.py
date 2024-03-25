from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

service = Service('/Users/and_seb/Documents/Programming/Chinese Language Classifier/chromedriver')
driver = webdriver.Chrome(service=service)

# # Specify the path to chromedriver.exe (download and save on your computer)
# service = Service('path/to/chromedriver')

# Set up options for the WebDriver
options = webdriver.ChromeOptions()
# options.add_argument('headless')  # Uncomment if you don't want the browser to open up

# Initialize the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open a webpage
driver.get("https://hskreading.com/the-tortoise-and-the-hare/")

# Wait for the dynamic content to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "ruby"))
)

# Get the page source
page_source = driver.page_source

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')

# Convert the entire page text to a string for searching
page_text = soup.get_text()

p_elements = soup.find_all('p')

for element in p_elements:
    print(element.text)  # Prints the text content of each <p> element

# Terms to search for
terms = ["HSK 1", "HSK 2", "HSK 3", "HSK 4", "HSK 5", "HSK 6"]

# Check if any of the terms are in the page text
for term in terms:
    if term in page_text:
        print(term)

  # Prints True if any term is found, False otherwise

# Find all ruby elements
ruby_elements = driver.find_elements(By.TAG_NAME, 'ruby')

# Similarly, if you want to find 'rt' elements:

# Now that the page is loaded, you can parse the HTML as required
elements = driver.find_elements(By.TAG_NAME, 'span')
for element in elements:
    print(element.text)

# Clean up: close the browser window
driver.quit()
