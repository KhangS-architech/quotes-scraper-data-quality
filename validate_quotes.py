import csv
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

required_columns = [
    "quote",
    "author",
    "tags",
    "source_page"
]

missing_columns = [
    column for column in required_columns
    if column not in (reader.fieldnames or [])
]

if missing_columns:
    print("Thiếu cột:", missing_columns)
    raise SystemExit(1)

total = len(rows)
missing_quotes = sum(
    not row["quote"].strip() for row in rows
)
missing_authors = sum(
    not row["author"].strip() for row in rows
)


non_empty_quotes = [
    row["quote"].strip()
    for row in rows
    if row["quote"].strip()
]

unique_quotes = set(non_empty_quotes)

duplicate_quote_rows = (
    len(non_empty_quotes) - len(unique_quotes)
)

print("=== INPUT DATA VALIDATION ===")
print("Total records:", total)
print("Missing quotes:", missing_quotes)
print("Missing authors:", missing_authors)
print("Unique non-empty quotes:", len(unique_quotes))
print("Duplicate non-empty quote rows:", duplicate_quote_rows)
