# N11.com Search Module - Load Test Scenarios

## Test Environment

| Parameter       | Value                          |
|-----------------|--------------------------------|
| Tool            | Apache JMeter 5.x              |
| Target          | https://www.n11.com            |
| Endpoint        | /arama?q={keyword}             |
| Virtual Users   | 1                              |
| Loop Count      | 1                              |
| Protocol        | HTTPS                          |
| Think Time      | 1000-2000ms between requests   |

## Test Scenarios

### Scenario 1: Open Homepage (Baseline)
- **Request**: `GET /`
- **Purpose**: Establish a session and baseline response time before performing searches
- **Assertions**:
  - No server error (HTTP 5xx)
  - Response time < 5000ms

### Scenario 2: Normal Product Search
- **Request**: `GET /arama?q=laptop`
- **Purpose**: Verify standard search functionality with a common product keyword
- **Assertions**:
  - No server error (HTTP 5xx)
  - Response time < 5000ms
- **Expected**: Search results page loads with relevant laptop products listed

### Scenario 3: Turkish Keyword Search
- **Request**: `GET /arama?q=telefon`
- **Purpose**: Verify search handles Turkish language keywords correctly, including proper UTF-8 encoding
- **Assertions**:
  - No server error (HTTP 5xx)
  - Response time < 5000ms
- **Expected**: Search returns Turkish-language product results for "telefon"

### Scenario 4: Multi-Word Search (Special Characters)
- **Request**: `GET /arama?q=samsung+galaxy`
- **Purpose**: Verify search handles multi-word queries with space encoding (URL-encoded as `+` or `%20`)
- **Assertions**:
  - No server error (HTTP 5xx)
  - Response time < 5000ms
- **Expected**: Search returns relevant Samsung Galaxy products

### Scenario 5: Empty Search Query (Edge Case)
- **Request**: `GET /arama?q=`
- **Purpose**: Verify the application handles empty search input gracefully without server errors
- **Assertions**:
  - Response code is NOT 500 (no server error)
  - Response time < 5000ms
- **Expected**: Application either redirects to homepage, shows a "please enter a search term" message, or displays a default product listing -- no 500 error

### Scenario 6: Long Text Search (Boundary Test)
- **Request**: `GET /arama?q=very+long+search+query+that+tests+the+limits+of+the+search+input+field`
- **Purpose**: Verify the search engine handles unusually long query strings without crashing or timing out
- **Assertions**:
  - Response code is NOT 500 (no server error)
  - Response time < 5000ms
- **Expected**: Application handles the long query gracefully, returning either a "no results" page or partial matches

## Metrics Collected

| Metric              | Description                                                |
|---------------------|------------------------------------------------------------|
| Response Time       | Time from request sent to last byte received (ms)          |
| Latency             | Time from request sent to first byte received (ms)         |
| Throughput          | Number of requests processed per second                    |
| Error Rate          | Percentage of requests that resulted in errors             |
| Bytes Sent/Received | Data volume transferred per request                        |
| Connect Time        | Time to establish TCP/SSL connection (ms)                  |

## How to Run

### GUI Mode (for debugging)
```bash
jmeter -t load_tests/n11_search_load_test.jmx
```

### CLI Mode (for actual test execution)
```bash
jmeter -n -t load_tests/n11_search_load_test.jmx -l results.jtl -e -o report/
```

### Parameters
| Flag | Description                                    |
|------|------------------------------------------------|
| `-n` | Non-GUI mode                                   |
| `-t` | Path to the .jmx test plan file                |
| `-l` | Path to the results log file (.jtl)            |
| `-e` | Generate HTML report after test                 |
| `-o` | Output directory for the HTML report            |

## Expected Results

| Scenario                  | Expected Status | Max Response Time |
|---------------------------|-----------------|-------------------|
| Open Homepage             | Not 5xx         | < 5000ms          |
| Search "laptop"           | Not 5xx         | < 5000ms          |
| Search "telefon"          | Not 5xx         | < 5000ms          |
| Search "samsung galaxy"   | Not 5xx         | < 5000ms          |
| Search empty query        | Not 5xx         | < 5000ms          |
| Search long text          | Not 5xx         | < 5000ms          |

## Pass/Fail Criteria

- **Pass**: All assertions pass, no server errors (5xx), all response times under 5 seconds
- **Fail**: Any server error (5xx) or response times exceeding 5 seconds
- **Note**: n11.com uses Cloudflare WAF which may return HTTP 403 for automated requests. This is expected WAF behavior, not a server error. Assertions are designed to detect actual server-side failures (5xx) rather than WAF responses.

## Notes

- The test uses 1 virtual user with 1 loop as specified in the case study requirements. Thread count can be increased for stress testing by modifying the Thread Group configuration.
- Constant timers (1000-2000ms) are placed between requests to simulate realistic user think time.
- HTTP Cookie Manager is enabled to handle session cookies automatically.
- UTF-8 encoding is set in HTTP Request Defaults to properly handle Turkish characters.
- The `follow_redirects` option is enabled to handle any server-side redirects transparently.
