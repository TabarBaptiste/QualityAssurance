import unittest
import csv
import os
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1 (in degrees)
        lat2, lon2: Latitude and longitude of point 2 (in degrees)
        
    Returns:
        float: Distance in kilometers
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def find_closest_radars(csv_file_path, lat, lon, limit=5):
    """
    Find the closest radars to a given location.
    
    Args:
        csv_file_path (str): Path to the CSV file containing radar data
        lat (float): Latitude of the reference point
        lon (float): Longitude of the reference point
        limit (int): Maximum number of radars to return
        
    Returns:
        list: List of tuples (radar_id, distance) sorted by distance
    """
    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"File not found: {csv_file_path}")
    
    radars = []
    
    with open(csv_file_path, 'r', encoding='latin-1') as file:
        csv_reader = csv.reader(file, delimiter=';')
        next(csv_reader)  # Skip header row
        
        for row in csv_reader:
            if len(row) >= 5 and row[3] and row[4]:  # Check if latitude and longitude exist
                try:
                    radar_id = row[0]
                    radar_lat = float(row[3])
                    radar_lon = float(row[4])
                    
                    distance = calculate_distance(lat, lon, radar_lat, radar_lon)
                    radars.append((radar_id, distance))
                except (ValueError, IndexError):
                    continue
    
    # Sort by distance and return the closest ones
    return sorted(radars, key=lambda x: x[1])[:limit]


class TestRadarGeo(unittest.TestCase):
    def setUp(self):
        # Path to the CSV file
        self.csv_file_path = os.path.join('data', 'jeu-de-donnees-liste-des-radars-fixes-en-france-2024-.csv')
    
    def test_calculate_distance(self):
        """Test the distance calculation function."""
        # Paris to Lyon (approximate coordinates)
        paris_lat, paris_lon = 48.8566, 2.3522
        lyon_lat, lyon_lon = 45.7640, 4.8357
        
        # The distance should be approximately 392 km
        distance = calculate_distance(paris_lat, paris_lon, lyon_lat, lyon_lon)
        self.assertAlmostEqual(distance, 392, delta=10)  # Allow 10 km margin of error
    
    def test_find_closest_radars(self):
        """Test finding the closest radars to a location."""
        # Paris coordinates
        paris_lat, paris_lon = 48.8566, 2.3522
        
        # Find the 3 closest radars to Paris
        closest_radars = find_closest_radars(self.csv_file_path, paris_lat, paris_lon, 3)
        
        # Verify we got the expected number of results
        self.assertEqual(len(closest_radars), 3, "Should find exactly 3 closest radars")
        
        # Verify the results are sorted by distance
        for i in range(1, len(closest_radars)):
            self.assertLessEqual(closest_radars[i-1][1], closest_radars[i][1], 
                               "Radars should be sorted by distance")
        
        # Verify all distances are reasonable (less than 1000 km from Paris)
        for radar_id, distance in closest_radars:
            self.assertLess(distance, 1000, f"Radar {radar_id} should be less than 1000 km from Paris")


if __name__ == '__main__':
    unittest.main()
