#!/usr/bin/env python3
'''test parameters'''
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
import json
import unittest
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


if __name__ == '__main__':
    unittest.main()
