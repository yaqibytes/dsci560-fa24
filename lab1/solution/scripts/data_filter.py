import os
import pandas as pd
from bs4 import BeautifulSoup

def get_data_directory():
    file_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(file_dir)
    data_dir = os.path.join(root_dir, "data")
    return data_dir

def read_raw_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")

def extract_latest_news(soup):
    latest_news = soup.find("ul", class_="LatestNews-list").find_all("li", class_="LatestNews-item")
    news_items = []
    for item in latest_news:
        headline = item.find("a", class_="LatestNews-headline")
        timestamp = item.find("time", class_="LatestNews-timestamp")
        if headline and timestamp:
            news_items.append({
                "timestamp": timestamp.text.strip(),
                "title": headline.get("title").strip(),
                "link": headline.get("href").strip()
            })
    return news_items

def extract_market_banner(soup):
    market_banner = soup.find("div", class_="MarketsBanner-marketData").find_all("a", class_="MarketCard-container")
    market_data = []
    for card in market_banner:
        symbol = card.find("span", class_="MarketCard-symbol")
        stock_position = card.find("span", class_="MarketCard-stockPosition")
        change_pts = card.find("span", class_="MarketCard-changesPts")
        if symbol and stock_position and change_pts:
            market_data.append({
                "symbol": symbol.text.strip(),
                "stock_position": float(stock_position.text.strip().replace(",", "")),
                "change_pts": float(change_pts.text.strip().replace(",", ""))
            })
    return market_data

def save_to_csv(data, filename):
    data_dir = os.path.join(get_data_directory(), "processed_data")
    os.makedirs(data_dir, exist_ok=True)
    pd.DataFrame(data).to_csv(os.path.join(data_dir, filename), index=False)

def main():
    print("Reading and parsing the raw HTML file...")
    EXTRACTED_HTML_PATH = os.path.join(get_data_directory(), "raw_data", "web_data.html")
    soup = read_raw_data(EXTRACTED_HTML_PATH)

    print("Extracting the latest news feed...")
    latest_news = extract_latest_news(soup)
    print("Saving the latest news feed data to CSV...")
    save_to_csv(latest_news, "news_data.csv")

    print("Extracting the market banner data...")
    market_banners = extract_market_banner(soup)
    print("Saving the market data to CSV...")
    save_to_csv(market_banners, "market_data.csv")

if __name__ == "__main__":
    main()
