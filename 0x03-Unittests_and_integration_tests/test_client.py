#!/usr/bin/env python3
'''test parameters'''
import unittest
from utils import access_nested_map, get_json, memoize
from client import GithubOrgClient
from parameterized import parameterized
from typing import Dict, Tuple, Union
from unittest import mock
from unittest.mock import patch, Mock, MagicMock, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([("google"), ("abc")])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        instance = GithubOrgClient(org_name)
        instance.org()
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


def test_public_repos_url(self):
    """Test that the result of _public_repos_url is the expected one based on the mocked payload"""
    with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
        payload = {'repos_url': 'https://api.github.com'}
        mock_org.return_value = payload
        instance = GithubOrgClient('google')
        self.assertEqual(instance._public_repos_url, payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        # Define the mock payload
        mock_payload = [{"name": "repo1"}, {"name": "repo2"}]
        
        # Mock get_json to return the mock payload
        mock_get_json.return_value = mock_payload
        
        # Mock _public_repos_url as a property
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"
            
            # Create an instance of GithubOrgClient
            instance = GithubOrgClient('google')
            
            # Call the public_repos method
            result = instance.public_repos()
            
            # Check that get_json was called once
            mock_get_json.assert_called_once()
            
            # Check that _public_repos_url property was accessed once
            self.assertEqual(mock_public_repos_url.call_count, 1)
            
            # Check that the result matches the expected list of repo names
            expected_repo_names = ["repo1", "repo2"]
            self.assertEqual(result, expected_repo_names)


if __name__ == '__main__':
    unittest.main()
