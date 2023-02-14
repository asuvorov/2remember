"""Define Test Cases."""

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class APIStatusTests(APITestCase):
    """Docstring."""

    def test_create_account(self):
        """Ensure we can create a new account object."""
        url = reverse("api-status")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APIVersionTests(APITestCase):
    """Docstring."""

    def test_create_account(self):
        """Ensure we can create a new account object."""
        url = reverse("api-version")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
