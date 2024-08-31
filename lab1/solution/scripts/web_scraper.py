import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

chrome_options = Options() 
chrome_options.add_argument("--headless")
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get('https://www.cnbc.com/world/?region=world')
    print("Page Title: ", driver.title)
finally:
    driver.quit()


