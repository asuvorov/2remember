"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""
try:
    from unittest import mock
except ImportError:
    import mock

import http.client

from datetime import timedelta

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login)
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.test import (
    TestCase,
    modify_settings,
    override_settings)

# pylint: disable=import-error
from app import (
    DAY_AGO,
    WEEK_AGO,
    MONTH_AGO,
    YEAR_AGO)
from organizations.decorators import (
    organization_create_access_check_required,
    organization_view_access_check_required,
    organization_edit_access_check_required)
from organizations.models import Organization
from tests import GenericUserTestCase


user_model = get_user_model()


class OrganizationCreateAccessCheckRequiredTest(GenericUserTestCase):

    """Test `organizations.decorators.organization_create_access_check_required` Decorator."""

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

        self.fnc = mock.MagicMock(return_value='fake response')
        self.decorated = organization_create_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="DAILY")
    def test_daily_admin(self):
        """Test `organizations.decorators.organization_create_access_check_required` against daily Limit.

        When Admin hits the daily Limit, he still can create a new Organization.
        This applies to other Limitations, so we check the Admin's Eligibility only once -
        against the daily Limit.
        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.admin)

        # ---------------------------------------------------------------------
        # --- Admin didn't hit the daily Limit, and IS allowed to create a new Organization.
        # ---------------------------------------------------------------------
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin hit the daily Limit, and still can create a new Organization.
        # ---------------------------------------------------------------------
        Organization.objects.create(author=self.admin, title="Organization #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="DAILY")
    def test_daily(self):
        """Test `organizations.decorators.organization_create_access_check_required` against daily Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the daily Limit, and IS allowed to create a new Organization.
        # ---------------------------------------------------------------------
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the daily Limit, and IS NOT allowed to create a new Organization.
        # ---------------------------------------------------------------------
        Organization.objects.create(author=self.john, title="Organization #1")
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="WEEKLY")
    def test_weekly(self):
        """Test `organizations.decorators.organization_create_access_check_required` against weekly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the weekly Limit, and IS allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #2")
        organization.created = WEEK_AGO - timedelta(days=2)
        organization.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the weekly Limit, and IS NOT allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #3")
        organization.created = WEEK_AGO + timedelta(days=2)
        organization.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="MONTHLY")
    def test_monthly(self):
        """Test `organizations.decorators.organization_create_access_check_required` against monthly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the monthly Limit, and IS allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)
        self.fnc.assert_called_once_with(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #2")
        organization.created = MONTH_AGO - timedelta(days=2)
        organization.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the monthly Limit, and IS NOT allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #3")
        organization.created = MONTH_AGO + timedelta(days=2)
        organization.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="YEARLY")
    def test_yearly(self):
        """Test `organizations.decorators.organization_create_access_check_required` against yearly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the yearly Limit, and IS allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #2")
        organization.created = YEAR_AGO - timedelta(days=2)
        organization.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the yearly Limit, and IS NOT allowed to create a new Organization.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #3")
        organization.created = YEAR_AGO + timedelta(days=2)
        organization.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)


class OrganizationViewAccessCheckRequiredTest(GenericUserTestCase):

    """Test `organizations.decorators.organization_view_access_check_required` Decorator."""

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

        self.fnc = mock.MagicMock(return_value='fake response')
        self.decorated = organization_view_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_public(self):
        """Test `organizations.decorators.organization_view_access_check_required` against public Organization."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.req_kwargs = {"slug":  organization.slug}

        # ---------------------------------------------------------------------
        # --- Author can view public Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author can view public Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.jane),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can view public Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_private(self):
        """Test `organizations.decorators.organization_view_access_check_required` against private Organization."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(
            author=self.john, title="Organization #1", is_private=True)
        self.req_kwargs = {"slug":  organization.slug}

        # ---------------------------------------------------------------------
        # --- Author can view private Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author CANNOT view private Organization.
        # ---------------------------------------------------------------------
        with self.assertRaises(PermissionDenied):
            self.decorated(
                self._generate_post_request(self.jane),
                *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can view private Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_retrieve(self):
        """Test `organizations.decorators.organization_view_access_check_required` retrieving Organization."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.req_kwargs = {}

        # ---------------------------------------------------------------------
        with self.assertRaises(Http404):
            self.decorated(
                self._generate_post_request(self.john),
                 *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john, data={"organization_uid": organization.uid}),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.req_kwargs = {"slug":  organization.slug}
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)


class OrganizationEditAccessCheckRequiredTest(GenericUserTestCase):

    """Test `organizations.decorators.organization_edit_access_check_required` Decorator."""

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

        self.fnc = mock.MagicMock(return_value='fake response')
        self.decorated = organization_edit_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_common(self):
        """Test `organizations.decorators.organization_edit_access_check_required` against Organization."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.req_kwargs = {"slug":  organization.slug}

        # ---------------------------------------------------------------------
        # --- Author can edit Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author CANNOT edit Organization.
        # ---------------------------------------------------------------------
        with self.assertRaises(PermissionDenied):
            self.decorated(
                self._generate_post_request(self.jane),
                *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can edit Organization.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_retrieve(self):
        """Test `organizations.decorators.organization_edit_access_check_required` retrieving Organization."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        organization = Organization.objects.create(author=self.john, title="Organization #1")
        self.req_kwargs = {}

        # ---------------------------------------------------------------------
        with self.assertRaises(Http404):
            self.decorated(
                self._generate_post_request(self.john),
                 *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john, data={"organization_uid": organization.uid}),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.req_kwargs = {"slug":  organization.slug}
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

"""
    self.assertEqual                /   self.assertNotEqual
    self.assertGreater
    self.assertGreaterEqual
    self.assertLess
    self.assertLessEqual
    self.assertTrue                 /   self.assertFalse
    self.assertIs                   /   self.assertIsNot
    self.assertIsNone               /   self.assertIsNotNone
    self.assertIn                   /   self.assertNotIn
    self.assertIsInstance           /   self.assertNotIsInstance
    self.assertRegexpMatches        /   self.assertNotRegexpMatches

    self.assertRaises
    self.assertRaisesMessage
    self.assertRaisesRegexp

    self.assertDictContainsSubset
    self.assertNumQueries

    self.assertContains             /   self.assertNotContains
    self.assertTemplateUsed         /   self.assertTemplateNotUsed
    self.assertInHTML
    self.assertJSONEqual            /   self.assertJSONNotEqual
"""
