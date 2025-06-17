import unittest
import csv
import os

# Function to analyze radar data
def analyze_radar_data(csv_file_path):
    """
    Analyzes radar data from a CSV file and returns statistics.
    
    Args:
        csv_file_path (str): Path to the CSV file containing radar data
        
    Returns:
        dict: Dictionary containing statistics about the radar data
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"File not found: {csv_file_path}")
    
    stats = {
        'total_radars': 0,
        'radar_types': {},
        'speed_limits': {},
        'avg_speed_limit': 0
    }
    
    speed_sum = 0
    speed_count = 0
    
    with open(csv_file_path, 'r', encoding='latin-1') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            stats['total_radars'] += 1
            
            # Count radar types
            radar_type = row[1] if len(row) > 1 else "Unknown"
            stats['radar_types'][radar_type] = stats['radar_types'].get(radar_type, 0) + 1
            
            # Count speed limits
            if len(row) > 5 and row[5]:
                try:
                    speed_limit = int(row[5])
                    stats['speed_limits'][speed_limit] = stats['speed_limits'].get(speed_limit, 0) + 1
                    speed_sum += speed_limit
                    speed_count += 1
                except ValueError:
                    pass
    
    # Calculate average speed limit
    if speed_count > 0:
        stats['avg_speed_limit'] = round(speed_sum / speed_count, 2)
    
    return stats


# Unit test class
class TestRadarAnalyzer(unittest.TestCase):
    def setUp(self):
        # Path to the CSV file
        self.csv_file_path = os.path.join('data', 'jeu-de-donnees-liste-des-radars-fixes-en-france-2024-.csv')
    
    def test_analyze_radar_data(self):
        """Test that the analyze_radar_data function correctly processes the radar data."""
        # Call the function
        stats = analyze_radar_data(self.csv_file_path)
        
        # Verify that we have statistics
        self.assertGreater(stats['total_radars'], 0, "Should have found radars in the CSV file")
        
        # Verify that we have radar types
        self.assertGreater(len(stats['radar_types']), 0, "Should have found radar types")
        
        # Verify that ETF, ETD, ETT, and ETFR types exist in the data
        self.assertIn('ETF', stats['radar_types'], "ETF radar type should exist")
        self.assertIn('ETD', stats['radar_types'], "ETD radar type should exist")
        self.assertIn('ETT', stats['radar_types'], "ETT radar type should exist")
        self.assertIn('ETFR', stats['radar_types'], "ETFR radar type should exist")
        
        # Verify that we have speed limits
        self.assertGreater(len(stats['speed_limits']), 0, "Should have found speed limits")
        
        # Verify that common speed limits exist
        common_speed_limits = [50, 70, 80, 90, 110, 130]
        for speed in common_speed_limits:
            self.assertIn(speed, stats['speed_limits'], f"Speed limit {speed} should exist")
        
        # Verify that the average speed limit is reasonable
        self.assertGreater(stats['avg_speed_limit'], 0, "Average speed limit should be greater than 0")
        self.assertLess(stats['avg_speed_limit'], 150, "Average speed limit should be less than 150")
    
    def test_file_not_found(self):
        """Test that the function raises FileNotFoundError when the file doesn't exist."""
        with self.assertRaises(FileNotFoundError):
            analyze_radar_data("non_existent_file.csv")


# Test runner
class MyTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = super().run(test)
        print(f"Total des tests: {result.testsRun}, Erreurs: {len(result.errors)}, Echecs: {len(result.failures)}")
        return result


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRadarAnalyzer)
    MyTestRunner().run(suite)
