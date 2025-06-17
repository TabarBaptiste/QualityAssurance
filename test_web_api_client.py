import unittest
import json
import os
from unittest.mock import patch, MagicMock
import requests
import pytest
import logging
import time
from functools import wraps

# Import the WebAPIClient class from the integration test file
from test_web_api_integration import WebAPIClient, measure_performance

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestWebAPIClient(unittest.TestCase):
    """Unit tests for the WebAPIClient class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        self.base_url = "https://api.example.com"
        self.api_key = "test_api_key"
        self.client = WebAPIClient(self.base_url, self.api_key)
    
    def tearDown(self):
        """Clean up after each test"""
        self.client.session.close()
    
    @measure_performance
    def test_init_with_api_key(self):
        """Test client initialization with API key"""
        client = WebAPIClient(self.base_url, self.api_key)
        self.assertEqual(client.base_url, self.base_url)
        self.assertEqual(client.api_key, self.api_key)
        self.assertIn("Authorization", client.session.headers)
        self.assertEqual(client.session.headers["Authorization"], f"Bearer {self.api_key}")
    
    @measure_performance
    def test_init_without_api_key(self):
        """Test client initialization without API key"""
        client = WebAPIClient(self.base_url)
        self.assertEqual(client.base_url, self.base_url)
        self.assertIsNone(client.api_key)
        self.assertNotIn("Authorization", client.session.headers)
    
    @measure_performance
    @patch('requests.Session.get')
    def test_get_method(self, mock_get):
        """Test the GET method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Test"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method
        result = self.client.get("items/1")
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.base_url}/items/1", params=None)
        self.assertEqual(result, {"id": 1, "name": "Test"})
    
    @measure_performance
    @patch('requests.Session.get')
    def test_get_with_params(self, mock_get):
        """Test the GET method with query parameters"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": [{"id": 1, "name": "Test"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the method with params
        params = {"filter": "active", "limit": 10}
        result = self.client.get("items", params=params)
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.base_url}/items", params=params)
        self.assertEqual(result, {"items": [{"id": 1, "name": "Test"}]})
    
    @measure_performance
    @patch('requests.Session.post')
    def test_post_method(self, mock_post):
        """Test the POST method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 2, "name": "New Item"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call the method
        data = {"name": "New Item"}
        result = self.client.post("items", data)
        
        # Assertions
        mock_post.assert_called_once_with(f"{self.base_url}/items", json=data)
        self.assertEqual(result, {"id": 2, "name": "New Item"})
    
    @measure_performance
    @patch('requests.Session.put')
    def test_put_method(self, mock_put):
        """Test the PUT method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Updated Item"}
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response
        
        # Call the method
        data = {"name": "Updated Item"}
        result = self.client.put("items/1", data)
        
        # Assertions
        mock_put.assert_called_once_with(f"{self.base_url}/items/1", json=data)
        self.assertEqual(result, {"id": 1, "name": "Updated Item"})
    
    @measure_performance
    @patch('requests.Session.delete')
    def test_delete_method(self, mock_delete):
        """Test the DELETE method"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the method
        result = self.client.delete("items/1")
        
        # Assertions
        mock_delete.assert_called_once_with(f"{self.base_url}/items/1")
        self.assertEqual(result, 204)
    
    @measure_performance
    @patch('requests.Session.get')
    def test_http_error_handling(self, mock_get):
        """Test handling of HTTP errors"""
        # Configure mock to raise an error
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")
        mock_get.return_value = mock_response
        
        # Call the method and expect an exception
        with self.assertRaises(requests.exceptions.HTTPError):
            self.client.get("nonexistent/123")
        
        mock_get.assert_called_once_with(f"{self.base_url}/nonexistent/123", params=None)
    
    @measure_performance
    @patch('requests.Session.get')
    def test_connection_error_handling(self, mock_get):
        """Test handling of connection errors"""
        # Configure mock to raise a connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        # Call the method and expect an exception
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.client.get("items/1")
        
        mock_get.assert_called_once_with(f"{self.base_url}/items/1", params=None)
    
    @measure_performance
    @patch('requests.Session.get')
    def test_timeout_error_handling(self, mock_get):
        """Test handling of timeout errors"""
        # Configure mock to raise a timeout error
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Call the method and expect an exception
        with self.assertRaises(requests.exceptions.Timeout):
            self.client.get("items/1")
        
        mock_get.assert_called_once_with(f"{self.base_url}/items/1", params=None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
