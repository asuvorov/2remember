"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import json
import unittest
import urllib.parse

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.test import (
    Client,
    TestCase,
    LiveServerTestCase)
from django.urls import reverse

import mock
import requests as request

from lxml import html
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APIRequestFactory,
    APIClient,
    APITestCase)
from termcolor import colored, cprint


api_factory = APIRequestFactory()
api_client = APIClient()
client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)


# =============================================================================
# ===
# === ATTACHMENTS
# ===
# =============================================================================
class TmpUploadViewSetTests(APITestCase):

    """TmpUploadViewSet Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Temporary Upload: User is not authorized."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        url = reverse("api-tmp-upload")
        data = {}

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        response = self.client.post(url, data, format="json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RemoveUploadViewSetTests(APITestCase):

    """RemoveUploadViewSet Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Remove Upload: User is not authorized."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        url = reverse("api-remove-upload")
        data = {
            "type":     "document",
            "id":       1,
        }

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        response = self.client.post(url, data, format="json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RemoveLinkViewSetTests(APITestCase):

    """RemoveLinkViewSet Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Remove Link: User is not authorized."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        url = reverse("api-remove-link")
        data = {
            "type":     "regular",
            "id":       1,
        }

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        response = self.client.post(url, data, format="json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

