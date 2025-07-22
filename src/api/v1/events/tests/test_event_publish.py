"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import json
import unittest
import urllib.parse

from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login)
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

from events.models import Event


api_factory = APIRequestFactory()
api_client = APIClient()
client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === EVENTS
# ===
# =============================================================================
class EventPublishViewSetTests(APITestCase):

    """EventPublishViewSet Test Class."""

    fixtures = [
        "test_accounts_users",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.event = Event.objects.create(
            author=self.john,
            title="Event #1")
        self.url = reverse("api-event-publish", kwargs={
            "event_id": self.event.id,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_not_authenticated(self):
        """Publish Event: User is not authenticated."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=None)
        response = api_client.post(self.url, self.data, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_event_not_found(self):
        """Publish Event: Event not found."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.jane)
        url = reverse("api-event-publish", kwargs={
            "event_id": 10,
        })
        response = api_client.post(url, self.data, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unauthorized(self):
        """Publish Event: User is not authorized to perform an Action."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.jane)
        response = api_client.post(self.url, self.data, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_success_author(self):
        """Publish Event: Success."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.john)
        response = api_client.post(self.url, self.data, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_success_admin(self):
        """Publish Event: Success."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.admin)
        response = api_client.post(self.url, self.data, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_200_OK)
