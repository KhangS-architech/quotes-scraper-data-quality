
# Quotes Scraper & Data Quality Pipeline

A Python-based web scraping and data enrichment project that collects quotes, verifies author profile information, enriches records with author biographies, and generates data quality reports.

## Project Overview

This project demonstrates an end-to-end data workflow using the practice website [Quotes to Scrape](https://quotes.toscrape.com/).

The pipeline collects quote records from multiple pages, validates author profile URLs, verifies author names against profile pages, extracts author biographies, and combines the collected information into an enriched dataset.

It also includes automated data validation, duplicate detection, completeness checks, and manual quality assurance.

## Project Objectives

- Collect structured data from a multi-page website.
- Validate and verify scraped information.
- Enrich existing records with additional information.
- Identify missing values and duplicate records.
- Produce structured CSV outputs for further analysis.
- Demonstrate a repeatable data collection and quality assurance workflow.

## Features

- **Web Scraping:** Extract quotes, author names, tags, source pages, and author profile URLs.
- **Pagination:** Collect records across multiple website pages.
- **URL Validation:** Check URL formats and test HTTP responses.
- **Author Verification:** Compare scraped author names with names displayed on author profile pages.
- **Data Enrichment:** Extract author biographies and associate them with quote records.
- **Data Validation:** Check required columns, missing quotes, missing authors, and duplicate quotes.
- **Data Quality Reporting:** Measure column completeness and identify invalid URLs and duplicate records.
- **Manual Quality Assurance:** Investigate records with missing tags and compare them with the source website.
- **CSV Export:** Save collected data, verification results, enriched records, and quality reports.

## Tools & Technologies

- Python
- Requests
- Beautiful Soup
- CSV
- pathlib
- Visual Studio Code

## Project Workflow

### 1. Scrape the Source Website

Collect quote records from multiple pages, including:

- Quote text
- Author name
- Tags
- Source page URL
- Author profile URL

Output: `quotes_data.csv`

### 2. Check Author URL Formats

Check whether author profile URLs are present and follow the expected URL format.

Script: `check_author_urls.py`

### 3. Verify Author URL Accessibility

Send HTTP requests to unique author profile URLs and record the results.

Script: `verify_author_urls.py`

Output: `author_url_report.csv`

### 4. Verify Author Names and Extract Biographies

Visit author profile pages, compare the displayed author names with the scraped names, and extract available biographies.

Script: `verify_author_names.py`

Output: `author_name_verification.csv`

### 5. Enrich the Quote Dataset

Match author biographies to quote records using author profile URLs.

Script: `enrich_quotes.py`

Output: `quotes_enriched.csv`

### 6. Validate the Input Dataset

Check required columns, missing quote text, missing author names, and duplicate non-empty quotes.

Script: `validate_quotes.py`

### 7. Generate a Data Quality Report

Measure field completeness, check author URL formats, and identify duplicate quote groups. Investigate missing tags against the source website.

Script: `data_quality_report.py`

Output: `data_quality_report.csv`

## Project Structure

```text
data-scraping-practice/
├── quotes_scraper.py
├── check_author_urls.py
├── verify_author_urls.py
├── verify_author_names.py
├── enrich_quotes.py
├── validate_quotes.py
├── data_quality_report.py
├── quotes_data.csv
├── author_url_report.csv
├── author_name_verification.csv
├── quotes_enriched.csv
├── data_quality_report.csv
├── requirements.txt
├── README.md
└── .gitignore
```

Generated files and local environment folders may differ depending on which scripts have been executed.

## Output Files

| File | Description |
|---|---|
| `quotes_data.csv` | Original scraped quote records |
| `author_url_report.csv` | Author URL accessibility verification results |
| `author_name_verification.csv` | Author name verification results and biographies |
| `quotes_enriched.csv` | Quote records enriched with author biographies |
| `data_quality_report.csv` | Column completeness and data quality summary |

## Current Results

Results from the current test run:

- **100** quote records collected across 10 pages.
- **50** unique author profile URLs checked.
- **50** author names matched after text normalization.
- **100** quote records enriched with non-empty author biographies.
- **0** invalid author URL formats reported in the final quality report.
- **0** duplicate quote groups detected in the enriched dataset.
- **0** missing quote values in the input validation check.
- **0** missing author values in the input validation check.
- **3** records had empty tags. Manual inspection indicated that the corresponding source quotes had no tags.

These results describe the current test dataset and may change if the source website or scraping logic changes.

## Getting Started

### Requirements

- Python 3 installed
- Internet access
- Git (optional, for version control)

### 1. Get the Project

Download or clone the repository, then open a terminal in the project directory.

### 2. Create a Virtual Environment

On Windows:

```powershell
py -m venv .venv
```

### 3. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use the virtual environment's Python executable directly instead.

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Pipeline

Run each script from the project root in the following order:

```bash
python quotes_scraper.py
python check_author_urls.py
python verify_author_urls.py
python verify_author_names.py
python enrich_quotes.py
python validate_quotes.py
python data_quality_report.py
```

On Windows, if the virtual environment is not activated, use:

```powershell
.\.venv\Scripts\python.exe quotes_scraper.py
```

Replace the script name with the relevant file for each step.

Some scripts depend on CSV files generated by earlier steps. Run the pipeline in order and make sure previous steps have completed successfully.

**Note:** Running `quotes_scraper.py` may overwrite `quotes_data.csv`. Back up any results you need to preserve before rerunning the scraper.

## Data Quality and Validation

The project uses several complementary checks:

- Required-column validation
- Missing-value checks
- URL format validation
- HTTP response checks
- Author name matching after normalization
- Duplicate quote detection
- Field completeness reporting
- Manual verification against source pages

Automated checks help identify potential issues but do not guarantee that every field is factually correct. Manual review remains important for validating extracted information.

## Limitations

- Results reflect the source website at the time of collection.
- HTTP success does not guarantee that a page contains the expected information.
- A valid URL format does not guarantee continued accessibility.
- Text normalization may not resolve every author-name variation.
- Empty tags may be valid when the source quote has no tags.
- The project has been tested on a small practice dataset, not at large scale.
- The workflow does not include a production database, scheduled execution, or automated monitoring.

## Responsible Scraping

- Respect the source website's terms, access rules, and applicable laws.
- Avoid excessive requests and unnecessary repeated downloads.
- Do not attempt to bypass authentication, access controls, or technical restrictions.
- Collect only information needed for the intended task.
- Review the source website's permissions before reusing or redistributing collected data.

This project is intended for learning and demonstrating data workflow skills.

## Skills Demonstrated

- Python scripting
- HTML parsing
- HTTP requests
- Multi-page web scraping
- CSV data processing
- URL validation and verification
- Text normalization
- Data enrichment and record matching
- Data quality checks
- Error handling
- Manual quality assurance
- Technical documentation

## Future Improvements

- Add configurable request timeouts and retry handling.
- Add automated tests for parsing, validation, and enrichment functions.
- Improve logging and error reporting.
- Add command-line options for input and output paths.
- Add a single command to run the complete pipeline.
- Add sample output previews and screenshots to the project documentation.

## Author

Created as a practical portfolio project to demonstrate web scraping, data enrichment, and data quality assurance using Python.
