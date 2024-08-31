import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_URL = "https://www.cnbc.com/world/?region=world"

def get_data_directory():
    file_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(file_dir)
    data_dir = os.path.join(root_dir, "data")
    return data_dir

def save_html_page(page_content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(page_content)

def main():
    # Setup Selenium with headless Chrome
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Load the page and wait for specific content to load
        driver.get(BASE_URL)
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "MarketCard-row"))
        )

        # Dynamic content using Selenium
        page = BeautifulSoup(driver.page_source, "html.parser")
        # Static content using requests
        response = requests.get(BASE_URL)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract desired content
        market_banner = page.find("div", class_="MarketsBanner-marketData").prettify()
        latest_news = soup.find("ul", class_="LatestNews-list").prettify()

        # Combine content for saving
        full_content = f"{market_banner}\n\n{latest_news}"

        # Save to file
        data_dir = get_data_directory()
        file_path = os.path.join(data_dir,"raw_data","web_data.html")
        save_html_page(full_content, file_path)

        print(f"HTML content saved to {file_path}")

    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
