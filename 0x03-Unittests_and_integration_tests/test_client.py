#!/usr/bin/env python3
'''test parameters'''
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
from unittest import mock
from unittest.mock import patch, PropertyMock, Mock


class TestGithubOrgClient(unittest.TestCase):
    """ Class for Testing Github Org Client """
    @parameterized.expand([("google"), ("abc")])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org"""
        instance = GithubOrgClient(org_name)
        instance.org()
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test that the result of _public_repos_url in mocked payload"""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            payload = {'repos_url': 'https://api.github.com'}
            mock_org.return_value = payload
            instance = GithubOrgClient('google')
            self.assertEqual(instance._public_repos_url, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload
        with patch.object(GithubOrgClient, '_public_repos_url',
                          new_callable=PropertyMock) as mock_org:
            mock_org.return_value = "https://api.github.com/orgs/google/repos"
            instance = GithubOrgClient('google')
            result = instance.public_repos()
            check = [i["name"] for i in payload]
            self.assertEqual(result, check)
            mock_get_json.assert_called_once()
            mock_org.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)])
    def test_has_license(self, repo, license_key, expected_result):
        """Test that the result of has_license in mocked payload"""
        self.assertEqual(GithubOrgClient.has_license(repo,
                                                     license_key), expected_result)

class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient using mock fixtures"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get"""
        cls.org_payload = org_payload
        cls.repos_payload = repos_payload
        cls.expected_repos = expected_repos
        cls.apache2_repos = apache2_repos
        
        # Mock requests.get with different side_effects
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()
        cls.mock_get.side_effect = [
            MockResponse(cls.org_payload),   # Mocking requests.get for org payload
            MockResponse(cls.repos_payload), # Mocking requests.get for repos payload
            MockResponse(cls.org_payload),   # Mocking requests.get for org payload again
            MockResponse(cls.repos_payload)  # Mocking requests.get for repos payload again
        ]

    def test_public_repos(self):
        """Test public_repos method without license filter"""
        # Create an instance of GithubOrgClient
        instance = GithubOrgClient('google')
        
        # Assertions
        self.assertEqual(instance.org(), self.org_payload)
        self.assertEqual(instance.repos_payload(), self.repos_payload)
        self.assertEqual(instance.public_repos(), self.expected_repos)
        self.assertEqual(instance.public_repos("XLICENSE"), [])
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """Test public_repos method with license filter"""
        # Create an instance of GithubOrgClient
        instance = GithubOrgClient('google')
        
        # Assertions
        self.assertEqual(instance.public_repos(), self.expected_repos)
        self.assertEqual(instance.public_repos("XLICENSE"), [])
        self.assertEqual(instance.public_repos("apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()

    @classmethod
    def tearDownClass(cls):
        """Tear down the mock"""
        cls.get_patcher.stop()

# Helper class to mock requests.get().json() responses
class MockResponse:
    def __init__(self, json_data):
        self.json_data = json_data
    
    def json(self):
        return self.json_data

if __name__ == '__main__':
    unittest.main()
