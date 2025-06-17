# Web API Testing Suite

This test suite provides comprehensive testing for web API integration, client functionality, and specific API endpoints.

## Test Architecture

The test suite follows a three-tier architecture:

1. **Test Cases**: Individual tests that verify specific functionality
2. **Test Suite**: Collection of test cases organized by category
3. **Test Runner**: Mechanism to discover, execute, and report test results

## Test Components

### Test Cases

- **test_web_api_integration.py**: Integration tests for the web API
  - `TestWebAPIIntegration` class with tests for:
    - API authentication
    - Error handling
    - Request validation
    - Response schema validation
    - Network conditions simulation
    - Concurrent API requests

- **test_web_api_client.py**: Unit tests for the WebAPIClient class
  - `TestWebAPIClient` class with tests for:
    - Client initialization
    - HTTP methods (GET, POST, PUT, DELETE)
    - Parameter handling
    - Error handling (HTTP, connection, timeout errors)

- **test_api_endpoints.py**: Tests for specific API endpoints
  - `TestAPIEndpoints` class with tests for:
    - Users endpoints (list, details, create, update, delete)
    - Products endpoints (list)
    - Orders endpoints (list)

### Test Suite

- **test_suite.py**: Organizes and manages test execution
  - `TestSuite` class that:
    - Discovers and loads test cases
    - Configures logging
    - Provides test result summary

### Test Runner

- **TestSuite.run_all_tests()**: Runs all discovered tests
- **TestSuite.run_specific_tests(pattern)**: Runs tests matching a pattern

## How to Run Tests

### Running All Tests

To run all tests in the suite:

```bash
python test_suite.py
```

### Running Specific Tests

To run specific tests by pattern:

```bash
python test_suite.py --pattern test_api_endpoints
```

### Command-line Arguments

- `--pattern`: Run only tests matching the specified pattern
- `--verbose` or `-v`: Increase output verbosity
- `--log-level`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

Example:

```bash
python test_suite.py --pattern test_web_api_client --verbose --log-level DEBUG
```

## Environment Variables

The following environment variables can be configured:

- `API_URL`: The URL of the API (default: https://api.example.com)
- `API_KEY`: The API key for authentication (default: test_key)

### Setting Environment Variables

#### Windows
```cmd
set API_URL=https://your-api-url.com
set API_KEY=your-api-key
```

#### Unix/Linux/macOS
```bash
export API_URL=https://your-api-url.com
export API_KEY=your-api-key
```

## Test Data Management

Test data is managed through the `TestDataManager` class, which ensures test isolation and idempotence. Test data is stored in JSON files:

- `test_data.json`: For integration tests
- `endpoint_test_data.json`: For endpoint-specific tests

## Utility Functions

### Performance Measurement

```python
@measure_performance
def test_method(self):
    # Test code here
```

The `measure_performance` decorator:
- Records the start time before executing the test
- Executes the test method
- Calculates the elapsed time after execution
- Logs the execution time with the test name
- Returns the original test result

### Network Simulation

```python
with simulate_network_condition(latency=0.1, packet_loss=0.2):
    # Code executed with simulated network conditions
```

The `simulate_network_condition` context manager:
- Patches the `requests.request` method
- Simulates network latency by adding delays
- Simulates packet loss by randomly raising connection errors
- Restores the original request method after execution

### Test Data Management

```python
data_manager = TestDataManager("test_data.json")
data_manager.create_test_data({"id": 1, "name": "Test Item"})
data_manager.get_test_data("id", 1)
data_manager.clear()
```

The `TestDataManager` class:
- Manages test data in JSON files
- Creates test data with unique identifiers
- Retrieves test data by key and value
- Clears test data after test execution

## Test Execution Workflow

1. **Test Discovery**:
   - The test runner scans for test files matching the pattern
   - Test classes and methods are identified

2. **Test Setup**:
   - `setUpClass()` is called once for each test class
   - Environment variables are loaded
   - Test resources are created
   - Mock objects are configured

3. **Test Execution**:
   - `setUp()` is called before each test method
   - The test method is executed with performance measurement
   - Assertions verify expected behavior
   - `tearDown()` is called after each test method

4. **Test Cleanup**:
   - `tearDownClass()` is called once after all tests in a class
   - Test resources are cleaned up
   - Mock objects are restored

5. **Result Reporting**:
   - Test results are logged to console and file
   - A summary report is generated

## Mocking Strategy

The test suite uses mocking extensively to avoid real network calls:

- `unittest.mock.patch`: Patches functions and methods
  ```python
  with patch('requests.get') as mock_get:
      mock_get.return_value = mock_response
      # Test code here
  ```

- `unittest.mock.MagicMock`: Creates mock objects with configurable behavior
  ```python
  mock_response = MagicMock()
  mock_response.json.return_value = {"id": 1, "name": "Test Item"}
  mock_response.status_code = 200
  ```

- `requests_mock`: Mocks HTTP requests and responses
  ```python
  with requests_mock.Mocker() as m:
      m.get('https://api.example.com/users', json={'users': []})
      # Test code here
  ```

## Logging

The test suite uses Python's built-in logging module to log test execution:

- Console logging: Shows test progress in real-time
- File logging: Stores detailed logs in `test_suite.log`

Log levels:
- DEBUG: Detailed debugging information
- INFO: Confirmation that things are working as expected
- WARNING: Indication that something unexpected happened
- ERROR: Due to a more serious problem, the software has not been able to perform a function
- CRITICAL: A serious error, indicating that the program itself may be unable to continue running

## Test Results

Test results are reported in several formats:

- Console output: Shows test status (pass/fail) and summary
- Log file: Contains detailed information about test execution
- Summary report: Shows total tests, failures, errors, and skipped tests

Example summary:
```
Test Suite Results:
  Start time: 2025-06-17 16:57:29.973148
  End time: 2025-06-17 16:57:30.191506
  Duration: 0.22 seconds
  Tests run: 27
  Failures: 0
  Errors: 0
  Skipped: 0
```
