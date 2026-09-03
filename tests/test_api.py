"""Integration tests for NewsTrace Flask REST endpoints."""
import unittest
from app import create_app
from config import get_config


class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app(get_config('testing'))
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_health_endpoint(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)

    def test_home_page(self):
        res = self.client.get('/')
        self.assertIn(res.status_code, [200, 302])


if __name__ == '__main__':
    unittest.main()

