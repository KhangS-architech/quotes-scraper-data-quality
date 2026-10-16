
import csv

QUOTES_FILE = "quotes_data.csv"
AUTHORS_FILE = "author_name_verification.csv"
OUTPUT_FILE = "quotes_enriched.csv"


def read_csv(filename):
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


quotes = read_csv(QUOTES_FILE)
authors = read_csv(AUTHORS_FILE)

# Tạo bảng tra cứu tiểu sử theo URL tác giả
bio_by_url = {}

for author in authors:
    author_url = author.get("author_url", "").strip()
    author_bio = author.get("author_bio", "").strip()

    if author_url:
        bio_by_url[author_url] = author_bio

# Ghép tiểu sử vào từng câu trích dẫn
for quote in quotes:
    author_url = quote.get("author_url", "").strip()
    quote["author_bio"] = bio_by_url.get(author_url, "")

# Giữ các cột cũ và thêm author_bio
fieldnames = list(quotes[0].keys())

if "author_bio" not in fieldnames:
    fieldnames.append("author_bio")

with open(OUTPUT_FILE, "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(quotes)

matched = sum(
    1 for quote in quotes if quote["author_bio"]
)

print("=== DATA ENRICHMENT REPORT ===")
print(f"Quotes processed: {len(quotes)}")
print(f"Quotes with author bio: {matched}")
print(f"Quotes without author bio: {len(quotes) - matched}")
print(f"Saved to: {OUTPUT_FILE}")
