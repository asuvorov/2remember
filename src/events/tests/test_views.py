"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import http.client
import pytest
import unittest

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

from app.models import Visibility
from events.models import Event
from organizations.models import Organization
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
class ListEventsTest(GenericUserTestCase):

    """Test list Events."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("event-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListDatelessEventsTest(GenericUserTestCase):

    """Test list dateless Events."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("event-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListMyProfileEventsTest(GenericUserTestCase):

    """Test list `My Profile` Events."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("event-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListForeignProfileEventsTest(GenericUserTestCase):

    """Test list `Foreign Profile` Events."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("event-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListOrganizationEventsTest(GenericUserTestCase):

    """Test list Organization Events."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("event-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


# =============================================================================
# ===
# === TEST CREATE EVENT
# ===
# =============================================================================
class CreateEventTest(GenericUserTestCase):

    """Test create Event."""

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

        self.url = reverse("event-create")
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_create_event(self):
        """Anonymous CANNOT create Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.login_url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "accounts/account-signin.html")

    def test_auth_can_create_event(self):
        """Authenticated User can create Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-create.html")

    def test_admin_can_create_event(self):
        """Admin can create Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.admin)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-create.html")


class CreateOrganizationEventTest(GenericUserTestCase):

    """Test create Organization Event."""

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

        self.organization = Organization.objects.create(
            author=self.john, title="Organization #1")
        self.url = reverse("event-create")
        self.login_url = reverse("signin")
        self.data = {"organization":    self.organization.uid}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    # @unittest.skip("Skip the Test. Waiting for Implementation to be merged.")
    def test_create_organization_event(self):
        """Authenticated User can create Organization Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-create.html")

        self.assertEqual(response.context["form"].fields["organization"].initial, self.organization)


# =============================================================================
# ===
# === TEST VIEW EVENT
# ===
# =============================================================================
class ViewPublicEventTest(GenericUserTestCase):

    """Test view Event Details."""

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
            "slug": self.event.slug,
        })
        self.data = {}

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
        response = client.get(self.url, data=self.data, follow=True)

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
        self.assertFalse(response.context["is_newly_created"])

    def test_author_can_view_event(self):
        """Author can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, data=self.data, follow=True)

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
        self.assertTrue(response.context["is_newly_created"])

    def test_non_author_can_view_event(self):
        """Non-Author can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.jane)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])

    def test_admin_can_view_event(self):
        """Admin can view public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.admin)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])


class ViewPrivateEventTest(GenericUserTestCase):

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

        self.event = Event.objects.create(
            author=self.john, title="Event #1", visibility=Visibility.PRIVATE)
        self.url = reverse("event-details", kwargs={
            "slug": self.event.slug,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_view_event(self):
        """Anonymous CANNOT view private Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.FORBIDDEN)
        self.assertTemplateUsed(response, "error-pages/403.html")

    def test_author_can_view_event(self):
        """Author can view private Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, data=self.data, follow=True)

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
        self.assertTrue(response.context["is_newly_created"])

    def test_non_author_cannot_view_event(self):
        """Non-Author CANNOT view private Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.jane)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.FORBIDDEN)
        self.assertTemplateUsed(response, "error-pages/403.html")

    def test_admin_can_view_event(self):
        """Admin can view private Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.admin)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-details-info.html")

        self.assertEqual(response.context["event"], self.event)
        self.assertIsNone(response.context["participation"])
        self.assertFalse(response.context["is_admin"])
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])


# =============================================================================
# ===
# === TEST EDIT EVENT
# ===
# =============================================================================
class EditEventTest(GenericUserTestCase):

    """Test edit Event."""

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
        self.url = reverse("event-edit", kwargs={
            "slug": self.event.slug,
        })
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_edit_event(self):
        """Anonymous CANNOT edit Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.FORBIDDEN)
        self.assertTemplateUsed(response, "error-pages/403.html")

    def test_author_can_edit_event(self):
        """Author can edit Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.john)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-edit.html")

        self.assertEqual(response.context["event"], self.event)

    def test_non_author_cannot_edit_event(self):
        """Non-Author CANNOT edit Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.jane)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.FORBIDDEN)
        self.assertTemplateUsed(response, "error-pages/403.html")

    def test_admin_can_edit_event(self):
        """Admin can edit Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        client.force_login(user=self.admin)
        response = client.get(self.url, data=self.data, follow=True)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.request["PATH_INFO"], self.url)
        self.assertEqual(response.status_code, http.client.OK)
        self.assertTemplateUsed(response, "events/event-edit.html")

        self.assertEqual(response.context["event"], self.event)
