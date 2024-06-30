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
        payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = payload
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = "https://api.github.com/orgs/google/repos"
            instance = GithubOrgClient('google')
            result = instance.public_repos()
            check = [i["name"] for i in payload]
            self.assertEqual(result, check)
            mock_get_json.assert_called_once()
            mock_org.assert_called_once()


if __name__ == '__main__':
    unittest.main()
