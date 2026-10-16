
import csv
from urllib.parse import urlparse
from pathlib import Path

INPUT_FILE = Path("quotes_data.csv")

if not INPUT_FILE.exists():
    print(f"Không tìm thấy file: {INPUT_FILE}")
    raise SystemExit(1)

with INPUT_FILE.open(
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:
    reader = csv.DictReader(file)
    rows = list(reader)

if not rows or "author_url" not in (reader.fieldnames or []):
    print("File trống hoặc không có cột author_url.")
    raise SystemExit(1)

total = len(rows)
missing = 0
invalid = 0
valid_format = 0
unique_urls = set()

for row in rows:
    url = row["author_url"].strip()

    if not url:
        missing += 1
        continue

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        invalid += 1
        print("URL sai định dạng:", url)
        continue

    valid_format += 1
    unique_urls.add(url)

print("\n=== AUTHOR URL REPORT ===")
print("Total records:", total)
print("Missing URLs:", missing)
print("Invalid URL formats:", invalid)
print("URLs with valid format:", valid_format)
print("Unique URLs:", len(unique_urls))
