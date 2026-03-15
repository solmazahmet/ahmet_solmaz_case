# InsiderOne - QA Automation Case Study

Test automation project covering UI testing, API testing, and load testing.

## Tech Stack

| Area        | Technology                          |
|-------------|-------------------------------------|
| UI Tests    | Python 3.11 + Selenium 4 + pytest   |
| API Tests   | Python 3.11 + requests + pytest     |
| Load Tests  | Apache JMeter 5.x                   |
| Reporting   | pytest-html                         |
| Pattern     | Page Object Model (POM)             |

## Project Structure

```
├── config/              # Configuration (URLs, timeouts)
├── pages/               # Page Object classes
│   ├── base_page.py     # Base class with common Selenium operations
│   ├── home_page.py     # Insider homepage
│   ├── careers_page.py  # Careers / QA department page
│   └── open_positions_page.py  # Job listings, filters
├── tests/
│   ├── ui/              # Selenium UI test cases
│   └── api/             # Petstore API test cases
├── load_tests/          # JMeter test plan and scenarios
│   ├── n11_search_load_test.jmx
│   └── test_scenarios.md
└── screenshots/         # Auto-captured on test failure
```

## Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running Tests

### UI Tests

```bash
# Chrome (default)
pytest tests/ui/ -v --html=report.html

# Firefox
pytest tests/ui/ -v --browser=firefox --html=report.html
```

Browser is parametrically changeable via `--browser` flag. Supported: `chrome`, `firefox`.

Screenshots are automatically captured in `screenshots/` directory when a test fails.
The filename includes the test name and timestamp (e.g. `test_home_page_is_loaded_20260315_142530.png`).

```bash
# List captured screenshots
ls screenshots/

# Open a specific screenshot (macOS)
open screenshots/<filename>.png
```

### API Tests

```bash
pytest tests/api/ -v
```

Tests Petstore API `/pet` endpoints with CRUD operations (positive and negative scenarios).

### Load Tests

Open the JMeter test plan in Apache JMeter GUI:
```bash
jmeter -t load_tests/n11_search_load_test.jmx
```

Or run headless from CLI:
```bash
jmeter -n -t load_tests/n11_search_load_test.jmx -l results.jtl -e -o report/
```

Test scenarios are documented in `load_tests/test_scenarios.md`.

### Run All pytest Tests

```bash
pytest -v --html=report.html
```

## Test Cases

### UI - Insider Careers Page
1. Verify home page loads with all main blocks (nav, hero, logos, footer)
2. Navigate to Careers > QA, click "See all QA jobs", verify QA job listings are present
3. Validate each job's Position and Department fields
4. Click "View Role" and verify redirect to Lever application form

### API - Petstore CRUD
- **Positive:** Create, Read, Update, Delete pet + find by status
- **Negative:** Invalid ID, malformed body, non-existent pet deletion, invalid status filter

### Load - n11.com Search
- Homepage baseline, normal search, Turkish keyword, multi-word, empty query, long text
- Assertions: HTTP status codes, response time < 5s, result container present

## Prerequisites

- Python 3.11+
- Chrome and/or Firefox browser installed
- Apache JMeter 5.x (for load tests only)
