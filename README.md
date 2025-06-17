# Quality, Testing and Maintenance for Web Applications

## Authors

- Harena ANDRIAMANANJARA MANDIMBY
- Andil ABAYOMI
- Elhadj Ibrahima BAH
- Baptiste TABAR LABONNE

## Project Description

This project demonstrates the use of different unit testing techniques in Python, using the `unittest` module. The tests are performed on a dataset of fixed speed cameras in France.

## Test File Structure

### 1. test_radar_analyzer.py

Test file that analyzes data from fixed speed cameras in France.

**Contents:**
- An `analyze_radar_data()` function that reads the CSV file and extracts statistics
- A `TestRadarAnalyzer` test class with two test methods:
  - `test_analyze_radar_data()`: Verifies that the data analysis works correctly
  - `test_file_not_found()`: Verifies that the function properly handles file not found errors

**Execution:**
```
python test_radar_analyzer.py
```

### 2. test_radar_geo.py

Test file that performs geographical calculations on the radar data.

**Contents:**
- A `calculate_distance()` function that calculates the distance between two geographical points
- A `find_closest_radars()` function that finds the closest radars to a given point
- A `TestRadarGeo` test class with two test methods:
  - `test_calculate_distance()`: Verifies that the distance calculation works correctly
  - `test_find_closest_radars()`: Verifies that the search for the closest radars works

**Execution:**
```
python test_radar_geo.py
```

### 3. test_suite.py

File that groups all tests into a test suite.

**Contents:**
- A `run_test_suite()` function that discovers and executes all tests
- Uses the unittest test discovery mechanism

**Execution:**
```
python test_suite.py
```

### 4. test_runner.py

File that provides an advanced test runner with reporting features.

**Contents:**
- A custom `TestResult` class that collects detailed information about test execution
- An `EnhancedTestRunner` class that provides detailed reports
- Supports text and HTML output formats
- Command-line options to customize test execution

**Execution:**
```
python test_runner.py
```

**Options:**
```
python test_runner.py --format html  # Generates an HTML report
python test_runner.py --verbosity 1  # Reduces verbosity
python test_runner.py --dir some_dir  # Runs tests in a specific directory
```

## Testing Concepts Demonstrated

1. **Unit Testing**: The smallest unit of testing. It checks for a specific response to a particular set of inputs.
2. **Test Suite**: Collection of multiple test cases or test suites
3. **Test Runner**: Component that orchestrates the execution of tests and provides results

## Data Used

The file `data/jeu-de-donnees-liste-des-radars-fixes-en-france-2024-.csv` contains data on fixed speed cameras in France, used for testing.
