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

urls = ['http://chinesereadingpractice.com/', 'http://chinesereadingpractice.com/page/2/', 'http://chinesereadingpractice.com/page/3/', 'http://chinesereadingpractice.com/page/4/',
        'http://chinesereadingpractice.com/page/5/', 'http://chinesereadingpractice.com/page/6/', 'http://chinesereadingpractice.com/page/7/']

for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all elements with the given class
    elements_with_class = soup.find_all(class_="entry-title heading-size-1")
    for element in elements_with_class:
        links = element.find_all('a', href=True)
        for link in links:
            with open('/Users/and_seb/Documents/Programming/Chinese Language Classifier/Chinese Reader Links.txt', 'a', encoding='utf-8') as file:
                file.write(link['href'])
                file.write("\n")
            
    
