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
from events.decorators import (
    event_create_access_check_required,
    event_view_access_check_required,
    event_edit_access_check_required)
from events.models import (
    Event,
    Visibility)
from tests import GenericUserTestCase


user_model = get_user_model()


class EventCreateAccessCheckRequiredTest(GenericUserTestCase):

    """Test `events.decorators.event_create_access_check_required` Decorator."""

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
        self.decorated = event_create_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="DAILY")
    def test_daily_admin(self):
        """Test `events.decorators.event_create_access_check_required` against daily Limit.

        When Admin hits the daily Limit, he still can create a new Event.
        This applies to other Limitations, so we check the Admin's Eligibility only once -
        against the daily Limit.
        """
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.admin)

        # ---------------------------------------------------------------------
        # --- Admin didn't hit the daily Limit, and IS allowed to create a new Event.
        # ---------------------------------------------------------------------
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin hit the daily Limit, and still can create a new Event.
        # ---------------------------------------------------------------------
        Event.objects.create(author=self.admin, title="Event #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="DAILY")
    def test_daily(self):
        """Test `events.decorators.event_create_access_check_required` against daily Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the daily Limit, and IS allowed to create a new Event.
        # ---------------------------------------------------------------------
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the daily Limit, and IS NOT allowed to create a new Event.
        # ---------------------------------------------------------------------
        Event.objects.create(author=self.john, title="Event #1")
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="WEEKLY")
    def test_weekly(self):
        """Test `events.decorators.event_create_access_check_required` against weekly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the weekly Limit, and IS allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #2")
        event.created = WEEK_AGO - timedelta(days=2)
        event.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the weekly Limit, and IS NOT allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #3")
        event.created = WEEK_AGO + timedelta(days=2)
        event.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="MONTHLY")
    def test_monthly(self):
        """Test `events.decorators.event_create_access_check_required` against monthly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the monthly Limit, and IS allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)
        self.fnc.assert_called_once_with(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #2")
        event.created = MONTH_AGO - timedelta(days=2)
        event.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the monthly Limit, and IS NOT allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #3")
        event.created = MONTH_AGO + timedelta(days=2)
        event.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)

    @override_settings(SUBSCRIPTION_PLAN_DEFAULT="YEARLY")
    def test_yearly(self):
        """Test `events.decorators.event_create_access_check_required` against yearly Limit."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        req = self._generate_post_request(self.john)

        # ---------------------------------------------------------------------
        # --- User didn't hit the yearly Limit, and IS allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #2")
        event.created = YEAR_AGO - timedelta(days=2)
        event.save()
        self.decorated(req, *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- User hit the yearly Limit, and IS NOT allowed to create a new Event.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #3")
        event.created = YEAR_AGO + timedelta(days=2)
        event.save()
        with self.assertRaises(PermissionDenied):
            self.decorated(req, *self.req_args, **self.req_kwargs)


class EventViewAccessCheckRequiredTest(GenericUserTestCase):

    """Test `events.decorators.event_view_access_check_required` Decorator."""

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
        self.decorated = event_view_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_public(self):
        """Test `events.decorators.event_view_access_check_required` against public Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.req_kwargs = {"slug":  event.slug}

        # ---------------------------------------------------------------------
        # --- Author can view public Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author can view public Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.jane),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can view public Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_private(self):
        """Test `events.decorators.event_view_access_check_required` against private Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        event = Event.objects.create(
            author=self.john, title="Event #1", visibility=Visibility.PRIVATE)
        self.req_kwargs = {"slug":  event.slug}

        # ---------------------------------------------------------------------
        # --- Author can view private Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author CANNOT view private Event.
        # ---------------------------------------------------------------------
        with self.assertRaises(PermissionDenied):
            self.decorated(
                self._generate_post_request(self.jane),
                *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can view private Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_retrieve(self):
        """Test `events.decorators.event_view_access_check_required` retrieving Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.req_kwargs = {}

        # ---------------------------------------------------------------------
        with self.assertRaises(Http404):
            self.decorated(
                self._generate_post_request(self.john),
                 *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john, data={"event_uid":  event.uid}),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.req_kwargs = {"slug":  event.slug}
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)


class EventEditAccessCheckRequiredTest(GenericUserTestCase):

    """Test `events.decorators.event_edit_access_check_required` Decorator."""

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
        self.decorated = event_edit_access_check_required(self.fnc)

        self.req_args = []
        self.req_kwargs = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_common(self):
        """Test `events.decorators.event_edit_access_check_required` against Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.req_kwargs = {"slug":  event.slug}

        # ---------------------------------------------------------------------
        # --- Author can edit Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Non-Author CANNOT edit Event.
        # ---------------------------------------------------------------------
        with self.assertRaises(PermissionDenied):
            self.decorated(
                self._generate_post_request(self.jane),
                *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        # --- Admin can edit Event.
        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.admin),
            *self.req_args, **self.req_kwargs)

    def test_retrieve(self):
        """Test `events.decorators.event_edit_access_check_required` retrieving Event."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        event = Event.objects.create(author=self.john, title="Event #1")
        self.req_kwargs = {}

        # ---------------------------------------------------------------------
        with self.assertRaises(Http404):
            self.decorated(
                self._generate_post_request(self.john),
                 *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.decorated(
            self._generate_post_request(self.john, data={"event_uid":  event.uid}),
            *self.req_args, **self.req_kwargs)

        # ---------------------------------------------------------------------
        self.req_kwargs = {"slug":  event.slug}
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
