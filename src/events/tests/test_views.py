"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import http.client
import pytest

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login)
from django.test import (
    Client,
    TestCase,
    LiveServerTestCase)
from django.urls import reverse

from rest_framework.test import APIClient
from termcolor import colored

from events.models import (
    Event,
    Visibility)
from tests import GenericUserTestCase


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST LIST EVENTS
# ===
# =============================================================================


# =============================================================================
# ===
# === TEST CREATE EVENT
# ===
# =============================================================================


# =============================================================================
# ===
# === TEST VIEW EVENT
# ===
# =============================================================================
class ViewPublicEventTest(GenericUserTestCase):

    """Test private Events."""

    fixtures = [
        "test_accounts_users",
        "test_accounts_profiles",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.event = Event.objects.create(author=self.john, title="Event #1")
        self.url = reverse("event-details", kwargs={
            "slug":     self.event.slug,
        })

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_can_view_event(self):
        """Anonymous can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        response = client.get(self.url, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])

    def test_author_can_view_event(self):
        """Author can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertTrue(response.context["is_admin"])
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])

    def test_non_author_can_view_event(self):
        """Non-Author can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.jane)
        response = client.get(self.url, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])

    def test_admin_can_view_event(self):
        """Admin can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.admin)
        response = client.get(self.url, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])


class ViewPrivateEventTest(GenericUserTestCase):

    """Test private Events."""

    fixtures = [
        "test_accounts_users",
        "test_accounts_profiles",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""


# =============================================================================
# ===
# === TEST EDIT EVENT
# ===
# =============================================================================
