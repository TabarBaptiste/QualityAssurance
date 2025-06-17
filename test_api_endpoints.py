import unittest
import json
import os
import time
import logging
from unittest.mock import patch, MagicMock
import requests
import pytest
from functools import wraps

# Import from existing test files
from test_web_api_integration import WebAPIClient, measure_performance, TestDataManager

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestAPIEndpoints(unittest.TestCase):
    """Tests for specific API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before all tests"""
        cls.api_url = os.environ.get("API_URL", "https://api.example.com")
        cls.api_key = os.environ.get("API_KEY", "test_key")
        cls.client = WebAPIClient(cls.api_url, cls.api_key)
        cls.data_manager = TestDataManager("endpoint_test_data.json")
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        cls.data_manager.clear()
    
    def setUp(self):
        """Set up before each test"""
        self.start_time = time.time()
    
    def tearDown(self):
        """Clean up after each test"""
        elapsed = time.time() - self.start_time
        logger.info(f"{self.id()} completed in {elapsed:.4f} seconds")
    
    @measure_performance
    @patch('requests.Session.get')
    def test_users_endpoint(self, mock_get):
        """Test the users endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "users": [
                {"id": 1, "username": "user1", "email": "user1@example.com"},
                {"id": 2, "username": "user2", "email": "user2@example.com"}
            ],
            "total": 2,
            "page": 1,
            "per_page": 10
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.get("users", params={"page": 1, "per_page": 10})
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.api_url}/users", params={"page": 1, "per_page": 10})
        self.assertEqual(len(result["users"]), 2)
        self.assertEqual(result["total"], 2)
        self.assertEqual(result["users"][0]["username"], "user1")
    
    @measure_performance
    @patch('requests.Session.get')
    def test_user_details_endpoint(self, mock_get):
        """Test the user details endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 1,
            "username": "user1",
            "email": "user1@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "created_at": "2025-01-01T12:00:00Z",
            "roles": ["user", "admin"]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.get("users/1")
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.api_url}/users/1", params=None)
        self.assertEqual(result["id"], 1)
        self.assertEqual(result["username"], "user1")
        self.assertEqual(result["email"], "user1@example.com")
        self.assertIn("admin", result["roles"])
    
    @measure_performance
    @patch('requests.Session.post')
    def test_create_user_endpoint(self, mock_post):
        """Test the create user endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 3,
            "username": "newuser",
            "email": "newuser@example.com",
            "created_at": "2025-06-17T14:30:00Z"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Data to send
        user_data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepassword",
            "first_name": "New",
            "last_name": "User"
        }
        
        # Call the endpoint
        result = self.client.post("users", user_data)
        
        # Assertions
        mock_post.assert_called_once_with(f"{self.api_url}/users", json=user_data)
        self.assertEqual(result["username"], user_data["username"])
        self.assertEqual(result["email"], user_data["email"])
        self.assertEqual(result["id"], 3)
    
    @measure_performance
    @patch('requests.Session.put')
    def test_update_user_endpoint(self, mock_put):
        """Test the update user endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "id": 1,
            "username": "user1",
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "updated_at": "2025-06-17T14:35:00Z"
        }
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response
        
        # Data to send
        update_data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User"
        }
        
        # Call the endpoint
        result = self.client.put("users/1", update_data)
        
        # Assertions
        mock_put.assert_called_once_with(f"{self.api_url}/users/1", json=update_data)
        self.assertEqual(result["email"], update_data["email"])
        self.assertEqual(result["first_name"], update_data["first_name"])
        self.assertEqual(result["last_name"], update_data["last_name"])
    
    @measure_performance
    @patch('requests.Session.delete')
    def test_delete_user_endpoint(self, mock_delete):
        """Test the delete user endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.status_code = 204
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # Call the endpoint
        result = self.client.delete("users/1")
        
        # Assertions
        mock_delete.assert_called_once_with(f"{self.api_url}/users/1")
        self.assertEqual(result, 204)
    
    @measure_performance
    @patch('requests.Session.get')
    def test_products_endpoint(self, mock_get):
        """Test the products endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "products": [
                {"id": 1, "name": "Product 1", "price": 19.99, "category": "electronics"},
                {"id": 2, "name": "Product 2", "price": 29.99, "category": "clothing"}
            ],
            "total": 2,
            "page": 1,
            "per_page": 10
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.get("products", params={"category": "all"})
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.api_url}/products", params={"category": "all"})
        self.assertEqual(len(result["products"]), 2)
        self.assertEqual(result["products"][0]["name"], "Product 1")
        self.assertEqual(result["products"][1]["category"], "clothing")
    
    @measure_performance
    @patch('requests.Session.get')
    def test_orders_endpoint(self, mock_get):
        """Test the orders endpoint"""
        # Configure mock
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "orders": [
                {
                    "id": 1, 
                    "user_id": 1, 
                    "total": 49.98,
                    "status": "completed",
                    "created_at": "2025-06-16T10:00:00Z",
                    "items": [
                        {"product_id": 1, "quantity": 1, "price": 19.99},
                        {"product_id": 2, "quantity": 1, "price": 29.99}
                    ]
                }
            ],
            "total": 1,
            "page": 1,
            "per_page": 10
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call the endpoint
        result = self.client.get("orders", params={"user_id": 1})
        
        # Assertions
        mock_get.assert_called_once_with(f"{self.api_url}/orders", params={"user_id": 1})
        self.assertEqual(len(result["orders"]), 1)
        self.assertEqual(result["orders"][0]["total"], 49.98)
        self.assertEqual(len(result["orders"][0]["items"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
