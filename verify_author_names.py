
import csv
import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

INPUT_FILE = Path("quotes_data.csv")
OUTPUT_FILE = Path("author_name_verification.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
}

# Đọc dữ liệu gốc
if not INPUT_FILE.exists():
    print("Không tìm thấy quotes_data.csv")
    raise SystemExit(1)

with INPUT_FILE.open(
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:
    reader = csv.DictReader(file)
    rows = list(reader)

required = {"author", "author_url"}
if not required.issubset(reader.fieldnames or []):
    print("CSV phải có cột author và author_url.")
    raise SystemExit(1)

# Một URL có thể xuất hiện ở nhiều câu trích dẫn.
# Lưu tên tác giả tương ứng cho từng URL.
url_to_authors = {}

for row in rows:
    url = row["author_url"].strip()
    author = row["author"].strip()

    if url:
        url_to_authors.setdefault(url, set()).add(author)

results = []

with requests.Session() as session:
    session.headers.update(HEADERS)

    for index, (url, expected_names) in enumerate(
        sorted(url_to_authors.items()), start=1
    ):
        print(f"[{index}/{len(url_to_authors)}] {url}")

        result = {
            "author_url": url,
            "csv_author_names": "; ".join(sorted(expected_names)),
            "page_author_name": "",
            "result": ""
        }

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            result["result"] = "invalid_url"
            results.append(result)
            continue

        try:
            response = session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            name_tag = soup.select_one(".author-title")
            bio_tag = soup.select_one(".author-description")
            author_bio = bio_tag.get_text(" ", strip=True) if bio_tag else ""
            result["author_bio"] = author_bio

            if not name_tag:
                result["result"] = "name_not_found"
            else:
                page_name = name_tag.get_text(strip=True)
                result["page_author_name"] = page_name

                # So sánh không phân biệt chữ hoa/thường,
                # bỏ khoảng trắng đầu/cuối.
                def normalize_name(name):
                    name = name.strip().casefold()
                    name = re.sub(r"[-\s]+", " ", name)
                    return name
                
                expected_normalized = {
                    normalize_name(name)
                    for name in expected_names
                }

                if normalize_name(page_name) in expected_normalized:
                    result["result"] = "match"
                else:
                    result["result"] = "mismatch"

        except requests.RequestException as error:
            result["result"] = "request_failed"
            print("  Request error:", error)

        results.append(result)

# Lưu báo cáo
fieldnames = [
    "author_url",
    "csv_author_names",
    "page_author_name",
    "author_bio",
    "result"
]

with OUTPUT_FILE.open(
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results)

print("\n=== AUTHOR NAME VERIFICATION ===")
print("Unique author URLs:", len(results))
print("Match:", sum(r["result"] == "match" for r in results))
print("Mismatch:", sum(r["result"] == "mismatch" for r in results))
print("Name not found:", sum(r["result"] == "name_not_found" for r in results))
print("Request failed:", sum(r["result"] == "request_failed" for r in results))
print("Report saved to:", OUTPUT_FILE)
