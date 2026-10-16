
import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

START_URL = "https://quotes.toscrape.com/"
OUTPUT_FILE = "quotes_data.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
}

# Lưu các bản ghi đã thu thập
all_quotes = []

# Bắt đầu từ trang đầu tiên
current_url = START_URL

while current_url:
    print(f"Đang scrape: {current_url}")

    response = requests.get(
        current_url,
        headers=HEADERS,
        timeout=20
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Tìm tất cả các khối trích dẫn trên trang
    quote_blocks = soup.select(".quote")

    for block in quote_blocks:
        quote_tag = block.select_one(".text")
        author_tag = block.select_one(".author")
        tag_elements = block.select(".tags .tag")

        quote_text = (
            quote_tag.get_text(strip=True)
            if quote_tag else ""
        )

       
        author = (
            author_tag.get_text(strip=True)
            if author_tag else ""
        )

        author_link = block.select_one(".author + a")
        author_url = ""

        if author_link and author_link.get("href"):
            author_url = urljoin(
                current_url,
                author_link["href"]
            )

        tags = "; ".join(
            tag.get_text(strip=True)
            for tag in tag_elements
        )

        all_quotes.append({
            "quote": quote_text,
            "author": author,
            "author_url": author_url,
            "tags": tags,
            "source_page": current_url
        })



    print(f"  Tìm thấy {len(quote_blocks)} bản ghi")

    # Tìm liên kết trang tiếp theo
    next_link = soup.select_one("li.next a")

    if next_link and next_link.get("href"):
        current_url = urljoin(
            current_url,
            next_link["href"]
        )
    else:
        current_url = None

# Xuất tất cả bản ghi ra CSV
fieldnames = [
    "quote",
    "author",
    "author_url",
    "tags",
    "source_page"
]

with open(
    OUTPUT_FILE,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )
    writer.writeheader()
    writer.writerows(all_quotes)

print("\nHoàn thành!")
print(f"Tổng số bản ghi: {len(all_quotes)}")
print(f"File đầu ra: {OUTPUT_FILE}")
