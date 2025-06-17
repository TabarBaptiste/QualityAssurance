import unittest
import os
import sys
import time
import argparse
from datetime import datetime
import html
import webbrowser
import tempfile

class TestResult(unittest.TextTestResult):
    """Custom TestResult class that collects more detailed information about test execution."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.test_results = []
        self.start_times = {}
        self.execution_times = {}
    
    def startTest(self, test):
        """Called when a test starts."""
        super().startTest(test)
        self.start_times[test] = time.time()
    
    def addSuccess(self, test):
        """Called when a test succeeds."""
        super().addSuccess(test)
        execution_time = time.time() - self.start_times[test]
        self.execution_times[test] = execution_time
        self.test_results.append({
            'test': test,
            'result': 'SUCCESS',
            'execution_time': execution_time,
            'details': None
        })
    
    def addError(self, test, err):
        """Called when a test raises an unexpected exception."""
        super().addError(test, err)
        execution_time = time.time() - self.start_times[test]
        self.execution_times[test] = execution_time
        self.test_results.append({
            'test': test,
            'result': 'ERROR',
            'execution_time': execution_time,
            'details': self._exc_info_to_string(err, test)
        })
    
    def addFailure(self, test, err):
        """Called when a test fails."""
        super().addFailure(test, err)
        execution_time = time.time() - self.start_times[test]
        self.execution_times[test] = execution_time
        self.test_results.append({
            'test': test,
            'result': 'FAILURE',
            'execution_time': execution_time,
            'details': self._exc_info_to_string(err, test)
        })
    
    def addSkip(self, test, reason):
        """Called when a test is skipped."""
        super().addSkip(test, reason)
        self.test_results.append({
            'test': test,
            'result': 'SKIP',
            'execution_time': 0,
            'details': reason
        })


class EnhancedTestRunner(unittest.TextTestRunner):
    """Enhanced test runner with detailed reporting capabilities."""
    
    def __init__(self, stream=None, descriptions=True, verbosity=1,
                 failfast=False, buffer=False, resultclass=None, warnings=None,
                 *, tb_locals=False, output_format='text'):
        self.output_format = output_format
        resultclass = resultclass or TestResult
        super().__init__(stream, descriptions, verbosity, failfast, buffer, resultclass, warnings, tb_locals=tb_locals)
    
    def run(self, test):
        """Run the tests."""
        start_time = time.time()
        result = super().run(test)
        execution_time = time.time() - start_time
        
        # Print summary to console
        self._print_summary(result, execution_time)
        
        # Generate report based on output format
        if self.output_format == 'html':
            self._generate_html_report(result, execution_time)
        
        return result
    
    def _print_summary(self, result, execution_time):
        """Print a summary of the test results to the console."""
        print("\n" + "=" * 70)
        print(f"TEST RUNNER SUMMARY")
        print("=" * 70)
        print(f"Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total Execution Time: {execution_time:.3f} seconds")
        print(f"Total Tests: {result.testsRun}")
        print(f"Successful: {result.testsRun - len(result.errors) - len(result.failures) - len(result.skipped)}")
        print(f"Errors: {len(result.errors)}")
        print(f"Failures: {len(result.failures)}")
        print(f"Skipped: {len(result.skipped)}")
        
        # Print test details
        if hasattr(result, 'test_results'):
            print("\nTEST DETAILS:")
            print("-" * 70)
            for test_result in result.test_results:
                test = test_result['test']
                status = test_result['result']
                execution_time = test_result['execution_time']
                
                status_color = {
                    'SUCCESS': '\033[92m',  # Green
                    'ERROR': '\033[91m',    # Red
                    'FAILURE': '\033[91m',  # Red
                    'SKIP': '\033[93m'      # Yellow
                }
                
                reset_color = '\033[0m'
                
                print(f"{status_color.get(status, '')}{status}{reset_color}: {test} ({execution_time:.3f}s)")
                
                if test_result['details']:
                    print(f"  Details: {test_result['details']}")
        
        print("=" * 70)
    
    def _generate_html_report(self, result, execution_time):
        """Generate an HTML report of the test results."""
        if not hasattr(result, 'test_results'):
            return
        
        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Results - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                .summary {{ background-color: #f5f5f5; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
                .test-details {{ margin-top: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .success {{ background-color: #dff0d8; }}
                .error, .failure {{ background-color: #f2dede; }}
                .skip {{ background-color: #fcf8e3; }}
                .details {{ font-family: monospace; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h1>Test Results</h1>
            
            <div class="summary">
                <h2>Summary</h2>
                <p>Run Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Total Execution Time: {execution_time:.3f} seconds</p>
                <p>Total Tests: {result.testsRun}</p>
                <p>Successful: {result.testsRun - len(result.errors) - len(result.failures) - len(result.skipped)}</p>
                <p>Errors: {len(result.errors)}</p>
                <p>Failures: {len(result.failures)}</p>
                <p>Skipped: {len(result.skipped)}</p>
            </div>
            
            <div class="test-details">
                <h2>Test Details</h2>
                <table>
                    <tr>
                        <th>Test</th>
                        <th>Result</th>
                        <th>Execution Time</th>
                        <th>Details</th>
                    </tr>
        """
        
        for test_result in result.test_results:
            test = test_result['test']
            status = test_result['result']
            execution_time = test_result['execution_time']
            details = test_result['details'] or ''
            
            html_content += f"""
                    <tr class="{status.lower()}">
                        <td>{test}</td>
                        <td>{status}</td>
                        <td>{execution_time:.3f}s</td>
                        <td class="details">{html.escape(str(details))}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        </body>
        </html>
        """
        
        # Write HTML to a temporary file and open in browser
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
            f.write(html_content)
            report_path = f.name
        
        print(f"\nHTML report generated: {report_path}")
        webbrowser.open('file://' + report_path)


def run_tests(start_dir=None, pattern="test_*.py", verbosity=2, output_format='text'):
    """
    Discover and run all tests in the specified directory.
    
    Args:
        start_dir: Directory to start discovery (default: current directory)
        pattern: Pattern to match test files (default: "test_*.py")
        verbosity: Verbosity level (0-2)
        output_format: Output format ('text' or 'html')
    
    Returns:
        unittest.TestResult: The test result object
    """
    if start_dir is None:
        start_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Discover tests
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir, pattern=pattern)
    
    # Run tests with our enhanced runner
    runner = EnhancedTestRunner(verbosity=verbosity, output_format=output_format)
    return runner.run(suite)


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run tests with enhanced reporting')
    parser.add_argument('--dir', default=None, help='Directory to start test discovery')
    parser.add_argument('--pattern', default='test_*.py', help='Pattern to match test files')
    parser.add_argument('--verbosity', type=int, default=2, choices=[0, 1, 2], help='Verbosity level')
    parser.add_argument('--format', choices=['text', 'html'], default='text', help='Output format')
    args = parser.parse_args()
    
    # Run tests
    result = run_tests(args.dir, args.pattern, args.verbosity, args.format)
    
    # Return exit code based on test results
    sys.exit(not result.wasSuccessful())
