from django.test import TestCase
from unittest.mock import patch, Mock
import requests

class MeEndpointTests(TestCase):

    @patch('core.views.requests.get')
    def test_me_returns_cat_fact_on_success(self, mock_get):
        # Setup mock response
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {'fact': 'Cats can rotate their ears 180 degrees.'}
        mock_get.return_value = mock_resp

        resp = self.client.get('/me')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('user', data)
        self.assertIn('email', data['user'])
        self.assertIn('timestamp', data)
        self.assertEqual(data['fact'], 'Cats can rotate their ears 180 degrees.')

    @patch('core.views.requests.get')
    def test_me_returns_fallback_when_external_api_fails(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout("timed out")
        resp = self.client.get('/me')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data['status'], 'success')
        self.assertTrue(data['fact'].startswith('Cat fact unavailable'))
