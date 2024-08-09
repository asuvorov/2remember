"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import http.client

from django.test import TestCase


class RobotsTest(TestCase):
    """Test `robots.txt`."""

    def test_get(self):
        """Test `robots.txt`."""
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, http.client.OK)
        self.assertEqual(response["content-type"], "text/plain")

    def test_post(self):
        """Test `robots.txt`."""
        response = self.client.post("/robots.txt")

        self.assertEqual(response.status_code, http.client.METHOD_NOT_ALLOWED)


class HumansTest(TestCase):
    """Test `humans.txt`."""

    def test_get(self):
        """Test `humans.txt`."""
        response = self.client.get("/humans.txt")

        self.assertEqual(response.status_code, http.client.OK)
        self.assertEqual(response["content-type"], "text/plain")

    def test_post(self):
        """Test `humans.txt`."""
        response = self.client.post("/humans.txt")

        self.assertEqual(response.status_code, http.client.METHOD_NOT_ALLOWED)
