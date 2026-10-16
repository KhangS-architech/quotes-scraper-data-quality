
import csv
from collections import Counter
from urllib.parse import urlparse

INPUT_FILE = "quotes_enriched.csv"
REPORT_FILE = "data_quality_report.csv"


def read_csv(filename):
    with open(filename, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def is_valid_url(value):
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except ValueError:
        return False


rows = read_csv(INPUT_FILE)

if not rows:
    raise SystemExit("Input CSV is empty.")

columns = list(rows[0].keys())
total_rows = len(rows)

print("=== DATA QUALITY REPORT ===")
print(f"Total records: {total_rows}")
print(f"Total columns: {len(columns)}")

report_rows = []

for column in columns:
    missing = sum(
        1 for row in rows
        if not row.get(column, "").strip()
    )

    complete = total_rows - missing
    completeness = complete / total_rows * 100

    report_rows.append({
        "column": column,
        "total_records": total_rows,
        "missing_values": missing,
        "complete_values": complete,
        "completeness_percent": round(completeness, 2),
    })

    print(
        f"{column}: {complete}/{total_rows} complete "
        f"({completeness:.2f}%), missing: {missing}"
    )

# Kiểm tra URL tác giả
url_values = [
    row.get("author_url", "").strip()
    for row in rows
    if row.get("author_url", "").strip()
]

invalid_urls = sum(
    1 for url in url_values
    if not is_valid_url(url)
)

# Đếm câu trích dẫn trùng nhau
quote_values = [
    row.get("quote", "").strip()
    for row in rows
    if row.get("quote", "").strip()
]

quote_counts = Counter(quote_values)
duplicate_quote_groups = sum(
    1 for count in quote_counts.values() if count > 1
)
duplicate_quote_rows = sum(
    count - 1 for count in quote_counts.values() if count > 1
)

print(f"Invalid author URLs: {invalid_urls}")
print(f"Duplicate quote groups: {duplicate_quote_groups}")
print(f"Extra duplicate quote rows: {duplicate_quote_rows}")

with open(REPORT_FILE, "w", encoding="utf-8-sig", newline="") as file:
    fieldnames = [
        "column",
        "total_records",
        "missing_values",
        "complete_values",
        "completeness_percent",
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(report_rows)

print(f"Saved column report to: {REPORT_FILE}")
print("\n=== RECORDS MISSING TAGS ===")

for index, row in enumerate(rows, start=2):
    if not row.get("tags", "").strip():
        print(
            f"CSV row {index} | "
            f"Author: {row.get('author', '')} | "
            f"Source: {row.get('source_page', '')} | "
            f"Quote: {row.get('quote', '')}"
        )