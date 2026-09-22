# Website Analytics & Link Crawler CLI (`analyze_links.py`)

A modular, high-performance command-line application in Python that crawls a website URL, extracts and classifies internal and external links, computes summary statistics (total links, latency, bytes transferred, broken links), and exports analytics reports in **Terminal ASCII Table**, **JSON**, or **CSV** format.

---

## ✨ Features

- **Multithreaded Concurrent Crawler**: Parallel HTTP fetching using Python's `concurrent.futures.ThreadPoolExecutor`.
- **Comprehensive Per-Link Metrics**: Link URL, Internal/External classification, HTTP Response Code, Latency (ms), Bytes Transferred, Content-Type, and Network/HTTP Error tracking.
- **Summary Analytics**: Aggregates total links, internal/external counts, broken links count (HTTP 4xx/5xx/errors), max response latency, and max bytes transferred.
- **Multiple Exporters**:
  - `terminal` (Default): ASCII summary box and detailed tabular report.
  - `json` (`--to=json`): Formatted JSON summary and array of link records.
  - `csv` (`--to=csv`): Standard CSV format for spreadsheets and data analysis.
- **Safe Bounded Crawling**:
  - Bounded crawl depth limit (`--max-depth`, default: 2).
  - Crawls internal links only; external links are fetched once for analysis without recursive traversal.
  - Visited URL tracking prevents infinite loops and duplicate HTTP requests.
  - Non-HTTP schemes (`mailto:`, `tel:`, `javascript:`, `#`) are cleanly filtered out.
- **Zero Browser Dependencies**: Pure HTTP requests via `httpx` and HTML parsing via `beautifulsoup4`.

---

## 🏗️ Architecture & Data Flow

```text
                    ┌──────────────────┐
                    │  Command Line    │
                    │   argparse       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  WebCrawler      │
                    │ThreadPoolExecutor│
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
          ┌─────────────┐        ┌─────────────┐
          │   Fetcher   │        │ URL Utils   │
          │    httpx    │        │ urllib      │
          └──────┬──────┘        └─────────────┘
                 │
                 ▼
          ┌─────────────┐
          │ HTML Parser │
          │ BeautifulSoup│
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │ LinkResults │
          │ @dataclass  │
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │  Analyzer   │
          └──────┬──────┘
                 │
                 ▼
          ┌─────────────┐
          │ Exporters / │
          │  Reporter   │
          ├─────────────┤
          │ Terminal    │
          │ JSON / CSV  │
          └─────────────┘
```

---

## 📁 Directory Structure

```text
p2 - web-analysis/
├── analyze_links.py          # CLI executable entry point
├── website_analytics/
│   ├── __init__.py
│   ├── cli.py                # argparse CLI parsing & execution flow
│   ├── models.py             # LinkResult & AnalyticsSummary dataclasses
│   ├── url_utils.py          # URL resolution, normalization, & domain policy
│   ├── fetcher.py            # httpx HTTP fetcher with latency/bytes timing
│   ├── parser.py             # BeautifulSoup HTML link extractor
│   ├── crawler.py            # ThreadPoolExecutor multi-threaded bounded crawler
│   ├── analyzer.py           # Summary statistics calculator
│   ├── reporter.py           # Terminal ASCII report generator
│   ├── exporters.py          # JSON and CSV export handlers
│   └── errors.py             # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── test_url_utils.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   ├── test_crawler.py
│   ├── test_analyzer.py
│   ├── test_exporters.py
│   └── test_cli.py
├── requirements.txt          # Production dependencies (httpx, beautifulsoup4)
├── requirements-dev.txt      # Development dependencies (pytest)
└── README.md                 # Project documentation
```

---

## 📦 Installation

Install required dependencies:

```bash
pip install -r requirements.txt
```

For development and running unit tests:

```bash
pip install -r requirements-dev.txt
```

---

## 🚀 Usage

### 1. Default Terminal Report
```bash
python analyze_links.py https://www.chandrashekar.info/
```

### 2. Export to JSON
```bash
python analyze_links.py https://www.python.org/ --to=json
```

### 3. Export to CSV
```bash
python analyze_links.py https://www.pypi.org/ --to=csv
```

### 4. Customizing Crawl Depth and Concurrency
```bash
python analyze_links.py https://example.com --max-depth=3 --workers=15 --timeout=5.0
```

---

## ⚙️ CLI Options

| Option | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `url` | `str` | *Required* | Target website URL to analyze |
| `--to` | `str` | `terminal` | Report output format (`terminal`, `json`, `csv`) |
| `--max-depth` | `int` | `2` | Maximum crawl depth for internal links |
| `--workers` | `int` | `10` | Number of concurrent worker threads |
| `--timeout` | `float` | `10.0` | HTTP request timeout in seconds |

---

## 📊 Output Formats

### Terminal ASCII Output
```text
+------------------------------------------------------------------------+
| Summary report:                                                        |
+------------------------------------------------------------------------+
|    Total Links: 67, Internal: 60, External: 7, Broken: 4               |
|    Max latency: 400ms, Max bytes transferred: 45,678 bytes             |
+------------------------------------------------------------------------+
| Detailed report:                                                       |
+----------------+-----+----------+---------+-------------+--------------+
|  Link          | E/I | Response | Latency | Bytes       | Content      |
|                |     | Code     | in ms   | Transferred | Type         |
+----------------+-----+----------+---------+-------------+--------------+
| /about         | I   | 200      | 256     | 45,232      | text/html    |
+----------------+-----+----------+---------+-------------+--------------+
```

### JSON Schema Output (`--to=json`)
```json
{
  "summary": {
    "total_links": 67,
    "internal_links": 60,
    "external_links": 7,
    "broken_links": 4,
    "max_latency_ms": 400.0,
    "max_bytes_transferred": 45678
  },
  "links": [
    {
      "url": "https://example.com/about",
      "type": "Internal",
      "status_code": 200,
      "latency_ms": 256.0,
      "bytes_transferred": 45232,
      "content_type": "text/html",
      "error": null
    }
  ]
}
```

---

## 🧪 Running Automated Tests

Tests use deterministic HTTP mocks (`httpx.MockTransport`) and do not require internet access:

```bash
pytest tests/
```

---

## 🔒 Limitations & Policy Decisions

1. **JavaScript Rendering**: Crawls static HTML pages parsed via BeautifulSoup. Pages relying on client-side JS single-page applications (SPAs) to inject links will only reveal links present in initial HTML.
2. **Bytes Transferred**: Represents HTTP response payload bytes actually received (`len(response.content)`).
3. **Internal vs External Domain Policy**: Links sharing the target's base domain or subdomains are classified as `Internal`. Distinct domains are classified as `External` and analyzed once without recursive link extraction.
