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
from collection.models import Collection
from events.models import Event
from organizations.models import Organization
from tests import GenericUserTestCase


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST LIST COLLECTIONS
# ===
# =============================================================================
class ListCollectionsTest(GenericUserTestCase):

    """Test list Collections."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("collection-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListDatelessCollectionsTest(GenericUserTestCase):

    """Test list dateless Collections."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("collection-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListMyProfileCollectionsTest(GenericUserTestCase):

    """Test list `My Profile` Collections."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("collection-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListForeignProfileCollectionsTest(GenericUserTestCase):

    """Test list `Foreign Profile` Collections."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("collection-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


class ListOrganizationCollectionsTest(GenericUserTestCase):

    """Test list Organization Collections."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("collection-list")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()


# =============================================================================
# ===
# === TEST LIST COLLECTION EVENTS
# ===
# =============================================================================


# =============================================================================
# ===
# === TEST CREATE COLLECTION
# ===
# =============================================================================
class CreateCollectionTest(GenericUserTestCase):

    """Test create Collection."""

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

        self.url = reverse("collection-create")
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_create_collection(self):
        """Anonymous CANNOT create Collection."""
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

    def test_auth_can_create_collection(self):
        """Authenticated User can create Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-create.html")

    def test_admin_can_create_collection(self):
        """Admin can create Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-create.html")


# =============================================================================
# ===
# === TEST VIEW COLLECTION
# ===
# =============================================================================
class ViewPublicCollectionTest(GenericUserTestCase):

    """Test view Collection Details."""

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

        self.collection = Collection.objects.create(author=self.john, title="Collection #1")
        self.url = reverse("collection-details", kwargs={
            "slug": self.collection.slug,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_can_view_collection(self):
        """Anonymous can view public Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])

    def test_author_can_view_collection(self):
        """Author can view public Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])
        self.assertTrue(response.context["is_newly_created"])

    def test_non_author_can_view_collection(self):
        """Non-Author can view public Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])

    def test_admin_can_view_collection(self):
        """Admin can view public Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])


class ViewPrivateCollectionTest(GenericUserTestCase):

    """Test private Collections."""

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

        self.collection = Collection.objects.create(
            author=self.john, title="Collection #1", visibility=Visibility.PRIVATE)
        self.url = reverse("collection-details", kwargs={
            "slug": self.collection.slug,
        })
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_view_collection(self):
        """Anonymous CANNOT view private Collection."""
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

    def test_author_can_view_collection(self):
        """Author can view private Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertFalse(response.context["show_rate_form"])
        self.assertFalse(response.context["show_complain_form"])
        self.assertTrue(response.context["is_newly_created"])

    def test_non_author_cannot_view_collection(self):
        """Non-Author CANNOT view private Collection."""
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

    def test_admin_can_view_collection(self):
        """Admin can view private Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-details-info.html")

        self.assertEqual(response.context["collection"], self.collection)
        self.assertTrue(response.context["show_rate_form"])
        self.assertTrue(response.context["show_complain_form"])
        self.assertFalse(response.context["is_newly_created"])


# =============================================================================
# ===
# === TEST EDIT COLLECTION
# ===
# =============================================================================
class EditCollectionTest(GenericUserTestCase):

    """Test edit Collection."""

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

        self.collection = Collection.objects.create(author=self.john, title="Collection #1")
        self.url = reverse("collection-edit", kwargs={
            "slug": self.collection.slug,
        })
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_anonymous_cannot_edit_collection(self):
        """Anonymous CANNOT edit Collection."""
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

    def test_author_can_edit_collection(self):
        """Author can edit Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-edit.html")

        self.assertEqual(response.context["collection"], self.collection)

    def test_non_author_cannot_edit_collection(self):
        """Non-Author CANNOT edit Collection."""
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

    def test_admin_can_edit_collection(self):
        """Admin can edit Collection."""
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
        self.assertTemplateUsed(response, "collections/collection-edit.html")

        self.assertEqual(response.context["collection"], self.collection)
