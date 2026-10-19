# Quotes Scraper & Data Quality Pipeline

A Python-based web scraping and data enrichment project that collects quotes from multiple web pages, verifies author profile information, enriches records with author biographies, and generates data quality reports.

## Project Overview

This project demonstrates an end-to-end data workflow using [Quotes to Scrape](https://quotes.toscrape.com/), a practice website for web scraping.

The pipeline collects structured quote records, validates author profile URLs, verifies author names against profile pages, extracts author biographies, and combines the collected information into an enriched dataset.

It also includes automated data validation, duplicate detection, completeness checks, execution logging, and manual quality assurance.

## Project Objectives

- Collect structured data from a multi-page website.
- Validate and verify scraped information.
- Enrich existing records with additional information.
- Identify missing values and duplicate records.
- Generate structured CSV outputs for further analysis.
- Automate the workflow with a single pipeline runner.
- Demonstrate a repeatable data collection and quality assurance process.

## Features

- **Web Scraping:** Extract quote text, author names, tags, source page URLs, and author profile URLs.
- **Pagination:** Collect records across multiple website pages.
- **URL Validation:** Check author URL formats and HTTP accessibility.
- **Author Verification:** Compare scraped author names with names displayed on author profile pages.
- **Data Enrichment:** Extract author biographies and associate them with quote records.
- **Data Validation:** Check required fields, missing values, and duplicate quotes.
- **Data Quality Reporting:** Measure field completeness and identify invalid URLs and duplicate records.
- **Manual Quality Assurance:** Investigate missing tags and compare records with the source website.
- **Pipeline Automation:** Run all seven processing scripts in sequence using one command.
- **Execution Logging:** Record timestamps, step durations, failures, and overall pipeline status.
- **CSV Export:** Save scraped data, verification results, enriched records, and quality reports.

## Tools & Technologies

- Python
- Requests
- Beautiful Soup
- CSV processing
- pathlib
- subprocess
- logging
- Visual Studio Code
- Git and GitHub

## Project Workflow

### 1. Scrape the Source Website

Collect quote records across multiple pages.

Fields collected:
- Quote text
- Author name
- Tags
- Source page URL
- Author profile URL

**Script:** `quotes_scraper.py`  
**Output:** `quotes_data.csv`

### 2. Check Author URL Formats

Check whether author profile URLs are present and follow the expected URL format.

**Script:** `check_author_urls.py`

### 3. Verify Author URL Accessibility

Send HTTP requests to unique author profile URLs and record accessibility results.

**Script:** `verify_author_urls.py`  
**Output:** `author_url_report.csv`

### 4. Verify Author Names and Extract Biographies

Visit author profile pages, compare displayed author names with scraped names, and extract available biographies.

**Script:** `verify_author_names.py`  
**Output:** `author_name_verification.csv`

### 5. Enrich the Quote Dataset

Match author biographies to quote records using author profile URLs.

**Script:** `enrich_quotes.py`  
**Output:** `quotes_enriched.csv`

### 6. Validate the Input Dataset

Check required columns, missing quote text, missing author names, and duplicate non-empty quotes.

**Script:** `validate_quotes.py`

### 7. Generate a Data Quality Report

Measure field completeness, check author URL formats, and identify duplicate quote groups. Missing tags are also investigated against the source website.

**Script:** `data_quality_report.py`  
**Output:** `data_quality_report.csv`

### 8. Run the Complete Pipeline

Execute all seven scripts in the correct order using a single command.

**Script:** `run_pipeline.py`  
**Log output:** `pipeline.log`

The pipeline runner:
- Executes each script in sequence.
- Stops if a script fails.
- Reports the current step and execution status.
- Records timestamps and step durations.
- Logs the total pipeline execution time.

## Project Structure

```text
quotes-scraper-data-quality/
├── quotes_scraper.py
├── check_author_urls.py
├── verify_author_urls.py
├── verify_author_names.py
├── enrich_quotes.py
├── validate_quotes.py
├── data_quality_report.py
├── run_pipeline.py
├── requirements.txt
├── README.md
└── .gitignore
```

The CSV files and `pipeline.log` are generated locally when the pipeline runs. They are excluded from version control by `.gitignore`.

## Output Files

| File | Description |
|---|---|
| `quotes_data.csv` | Original scraped quote records |
| `author_url_report.csv` | Author URL accessibility results |
| `author_name_verification.csv` | Author name verification results and biographies |
| `quotes_enriched.csv` | Quote records enriched with author biographies |
| `data_quality_report.csv` | Field completeness and data quality summary |
| `pipeline.log` | Execution timestamps, durations, and pipeline status |

## Current Results

Results from the current test run:

- **100 quote records** collected across 10 pages.
- **50 unique author profile URLs** checked.
- **50 author names** matched after text normalization.
- **100 quote records** enriched with non-empty author biographies.
- **0 invalid author URL formats** reported in the final quality report.
- **0 duplicate quote groups** detected in the enriched dataset.
- **0 missing quote values** in the input validation check.
- **0 missing author values** in the input validation check.
- **3 records with empty tags**, manually checked against the source website and confirmed to have no tags.

The complete pipeline finished successfully in approximately **88 seconds** during one test run. Execution time may vary depending on network conditions and source website response times.

These results describe the current test dataset and may change if the source website or scraping logic changes.

## Getting Started

### Requirements

- Python 3
- Internet access
- Git (optional, for cloning the repository)

### 1. Clone the Repository

```bash
git clone https://github.com/KhangS-architech/quotes-scraper-data-quality.git
cd quotes-scraper-data-quality
```

Alternatively, download the repository as a ZIP file and extract it.

### 2. Create a Virtual Environment

On Windows:

```powershell
py -m venv .venv
```

### 3. Activate the Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script activation, use the virtual environment's Python executable directly.

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run the Complete Pipeline

From the project root, run:

```bash
python run_pipeline.py
```

The runner executes all seven processing scripts in sequence. Generated CSV files are saved locally, and execution logs are written to `pipeline.log`.

To inspect the results, open the generated CSV files in a spreadsheet application or text editor.

**Important:** Running the scraper may overwrite existing output files, including `quotes_data.csv`. Back up any results you need to preserve before rerunning the pipeline.

## Data Quality and Validation

The project uses several complementary checks:

- Required-column validation
- Missing-value checks
- URL format validation
- HTTP response checks
- Author name matching after text normalization
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
- Network latency and source website changes may affect execution time and results.

## Responsible Scraping

- Respect the source website's terms, access rules, and applicable laws.
- Avoid excessive requests and unnecessary repeated downloads.
- Do not attempt to bypass authentication, access controls, or technical restrictions.
- Collect only information needed for the intended task.
- Review source website permissions before reusing or redistributing collected data.

This project is intended for learning and demonstrating web scraping, data enrichment, and data quality assurance skills.

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
- Pipeline orchestration
- Logging and error handling
- Manual quality assurance
- Technical documentation
- Git and GitHub version control

## Future Improvements

- Add configurable request timeouts and retry handling.
- Add automated tests for parsing, validation, and enrichment functions.
- Improve logging and error reporting.
- Add command-line options for input and output paths.
- Add sample output previews and screenshots to the project documentation.
- Improve resilience to source website changes.

## Author

Created as a practical portfolio project to demonstrate web scraping, data enrichment, pipeline automation, and data quality assurance using Python.