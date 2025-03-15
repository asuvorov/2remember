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

from events.models import Event
from organizations.models import Organization
from tests import GenericUserTestCase


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST LIST ORGANIZATIONS
# ===
# =============================================================================
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

        self.url = reverse("organization-organizations")
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


# =============================================================================
# ===
# === TEST ORGANIZATIONS DIRECTORY
# ===
# =============================================================================


# =============================================================================
# ===
# === TEST CREATE ORGANIZATION
# ===
# =============================================================================
class CreateOrganizationTest(GenericUserTestCase):

    """Test create Organization."""

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

        self.url = reverse("organization-create")
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_create_organization(self):
        """Anonymous CANNOT create Organization."""
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

    def test_auth_can_create_organization(self):
        """Authenticated User can create Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-create.html")

    def test_admin_can_create_organization(self):
        """Admin can create Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-create.html")


# =============================================================================
# ===
# === TEST VIEW ORGANIZATION
# ===
# =============================================================================
class ViewPublicOrganizationTest(GenericUserTestCase):

    """Test view Organization Details."""

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

        self.organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.url = reverse("organization-details", kwargs={
            "slug": self.organization.slug,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_can_view_organization(self):
        """Anonymous can view public Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_author_can_view_organization(self):
        """Author can view public Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_non_author_can_view_organization(self):
        """Non-Author can view public Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_admin_can_view_organization(self):
        """Admin can view public Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)


class ViewPrivateOrganizationTest(GenericUserTestCase):

    """Test private Organizations."""

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
            author=self.john, title="Organization #1", is_private=True)
        self.url = reverse("organization-details", kwargs={
            "slug": self.organization.slug,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_view_organization(self):
        """Anonymous CANNOT view private Organization."""
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

    def test_author_can_view_organization(self):
        """Author can view private Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_non_author_cannot_view_organization(self):
        """Non-Author CANNOT view private Organization."""
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

    def test_admin_can_view_organization(self):
        """Admin can view private Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-details-info.html")

        self.assertEqual(response.context["organization"], self.organization)


# =============================================================================
# ===
# === TEST EDIT ORGANIZATION
# ===
# =============================================================================
class EditOrganizationTest(GenericUserTestCase):

    """Test edit Organization."""

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

        self.organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.url = reverse("organization-edit", kwargs={
            "slug": self.organization.slug,
        })
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_edit_organization(self):
        """Anonymous CANNOT edit Organization."""
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

    def test_author_can_edit_organization(self):
        """Author can edit Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-edit.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_non_author_cannot_edit_organization(self):
        """Non-Author CANNOT edit Organization."""
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

    def test_admin_can_edit_organization(self):
        """Admin can edit Organization."""
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
        self.assertTemplateUsed(response, "organizations/organization-edit.html")

        self.assertEqual(response.context["organization"], self.organization)


# =============================================================================
# ===
# === TEST POPULATE ORGANIZATION NEWSLETTER
# ===
# =============================================================================
class PopulateOrganizationNewsletterTest(GenericUserTestCase):

    """Test populate Organization Newsletter."""

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

        self.organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.url = reverse("organization-populate-newsletter", kwargs={
            "slug": self.organization.slug,
        })
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_populate_organization_newsletter(self):
        """Anonymous CANNOT populate Organization Newsletter."""
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

    def test_author_can_populate_organization_newsletter(self):
        """Author can populate Organization Newsletter."""
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
        self.assertTemplateUsed(response, "organizations/organization-populate-newsletter.html")

        self.assertEqual(response.context["organization"], self.organization)

    def test_non_author_cannot_populate_organization_newsletter(self):
        """Non-Author CANNOT populate Organization Newsletter."""
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

    def test_admin_can_populate_organization_newsletter(self):
        """Admin can populate Organization Newsletter."""
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
        self.assertTemplateUsed(response, "organizations/organization-populate-newsletter.html")

        self.assertEqual(response.context["organization"], self.organization)
