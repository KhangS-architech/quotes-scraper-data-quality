
import csv
import requests
from pathlib import Path
from urllib.parse import urlparse

INPUT_FILE = Path("quotes_data.csv")
OUTPUT_FILE = Path("author_url_report.csv")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; LearningScraper/1.0)"
}

if not INPUT_FILE.exists():
    print(f"Không tìm thấy file: {INPUT_FILE}")
    raise SystemExit(1)

with INPUT_FILE.open(
    "r",
    newline="",
    encoding="utf-8-sig"
) as file:
    reader = csv.DictReader(file)

    if "author_url" not in (reader.fieldnames or []):
        print("Thiếu cột author_url.")
        raise SystemExit(1)

    rows = list(reader)

urls = sorted({
    row["author_url"].strip()
    for row in rows
    if row.get("author_url", "").strip()
})

results = []

with requests.Session() as session:
    session.headers.update(HEADERS)

    for index, url in enumerate(urls, start=1):
        print(f"[{index}/{len(urls)}] Kiểm tra: {url}")

        result = {
            "author_url": url,
            "http_status": "",
            "final_url": "",
            "result": ""
        }

        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            result["result"] = "invalid_format"
        else:
            try:
                response = session.get(
                    url,
                    timeout=15,
                    allow_redirects=True
                )

                result["http_status"] = response.status_code
                result["final_url"] = response.url

                if 200 <= response.status_code < 300:
                    result["result"] = "http_success"
                else:
                    result["result"] = "http_error"

            except requests.RequestException as error:
                result["result"] = "request_failed"
                print("  Lỗi:", error)

        results.append(result)

with OUTPUT_FILE.open(
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:
    writer = csv.DictWriter(
        file,
        fieldnames=[
            "author_url",
            "http_status",
            "final_url",
            "result"
        ]
    )
    writer.writeheader()
    writer.writerows(results)

print("\n=== URL VERIFICATION REPORT ===")
print("Unique URLs checked:", len(urls))
print("HTTP success:", sum(
    r["result"] == "http_success" for r in results
))
print("HTTP error:", sum(
    r["result"] == "http_error" for r in results
))
print("Request failed:", sum(
    r["result"] == "request_failed" for r in results
))
print("Saved to:", OUTPUT_FILE)
