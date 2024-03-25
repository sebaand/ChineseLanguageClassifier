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


with open('/Users/and_seb/Documents/Programming/Chinese Language Classifier/Web Scraping/Links for Scraping/YesChineseInternal.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# urls = ['http://chinesereadingpractice.com/', 'http://chinesereadingpractice.com/page/2/', 'http://chinesereadingpractice.com/page/3/', 'http://chinesereadingpractice.com/page/4/',
#         'http://chinesereadingpractice.com/page/5/', 'http://chinesereadingpractice.com/page/6/', 'http://chinesereadingpractice.com/page/7/']

HSK3 = ["GR-03","GR-04"]
HSK4 = ["GR-05","GR-06","GR-07"]
HSK5 = ["GR-08","GR-09","GR-10","GR-11"]
HSK6 = ["GR-12"]
for url in urls:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract all elements with the given class
    elements_with_class = soup.find_all(class_="desc")
    for element in elements_with_class:
        links = element.find_all('a', href=True)
        for link in links:
            with open('/Users/and_seb/Documents/Programming/Chinese Language Classifier/YesChinese Links.txt', 'a', encoding='utf-8') as file:
                file.write(link['href'])
                file.write("\n")
                for i in range(len(HSK3)):
                    if HSK3[i] in url:
                        file.write("HSK3\n")
                for i in range(len(HSK4)):
                    if HSK4[i] in url:
                        file.write("HSK4\n")
                for i in range(len(HSK5)):
                    if HSK5[i] in url:
                        file.write("HSK5\n")
                for i in range(len(HSK6)):
                    if HSK6[i] in url:
                        file.write("HSK6\n")
            
    
