"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
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
# === MOCKS
# ===
# =============================================================================


# =============================================================================
# ===
# === MODELS
# ===
# =============================================================================


# =============================================================================
# ===
# === VIEWS
# ===
# =============================================================================
class AccountsListViewTestCase(TestCase):

    """Accounts List Test Case."""

    fixtures = [
        "test_accounts_users.json",
        "test_accounts_profiles.json",
        "test_accounts_privacy_basic.json",
        "test_core_addresses_accounts.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ACCOUNTS > VIEWS > LIST", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("account-list")

        # --- Users
        self.test_user_1 = User.objects.get(id=1)
        self.test_user_2 = User.objects.get(id=2)
        self.test_user_3 = User.objects.get(id=3)
        self.test_user_4 = User.objects.get(id=4)

    def test_user_not_logged_in(self):
        """Account List. User NOT logged in."""
        cprint("[---  INFO   ---] Test Account List. User NOT logged in...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        # cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context["organizations"], "yellow")
        # cprint("[---  DUMP   ---] REQUEST          : %s" % response.request, "yellow")
        # cprint("[---  DUMP   ---] STATUS           : %s" % response.status_code, "yellow")
        # cprint("[---  DUMP   ---] TEMPLATES        : %s" % response.templates, "yellow")
        # cprint("[---  DUMP   ---] CONTENT          : %s" % response.content, "yellow")
        # cprint("[---  DUMP   ---] REDIRECT CHAIN   : %s" % response.redirect_chain, "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["accounts"]),
            len(User.objects.filter(
                is_active=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))

    def test_user_logged_in(self):
        """Account List. User logged in. Simple Case."""
        cprint("[---  INFO   ---] Test Account List. User logged in. Simple Case...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        # cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context["organizations"], "yellow")
        # cprint("[---  DUMP   ---] REQUEST          : %s" % response.request, "yellow")
        # cprint("[---  DUMP   ---] STATUS           : %s" % response.status_code, "yellow")
        # cprint("[---  DUMP   ---] TEMPLATES        : %s" % response.templates, "yellow")
        # cprint("[---  DUMP   ---] CONTENT          : %s" % response.content, "yellow")
        # cprint("[---  DUMP   ---] REDIRECT CHAIN   : %s" % response.redirect_chain, "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["accounts"]),
            len(User.objects.filter(
                is_active=True,
            ).exclude(
                id=self.test_user_1.id,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))


class AccountLoginViewTestCase(TestCase):

    """Log in Test Case."""

    fixtures = [
        "test_accounts_users.json",
        "test_accounts_profiles.json",
        "test_core_addresses_accounts.json"
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ACCOUNTS > VIEWS", "green")

        # ---------------------------------------------------------------------
        # --- Fake

    def test_account_login(self):
        """Log in."""
        cprint("[---  INFO   ---] Test Account Log in...", "cyan")

        url = reverse("login")
        data = {}
        response = client.post(
            url,
            data=data)

        # ---------------------------------------------------------------------
        # --- Test Response


# =============================================================================
# ===
# === AJAX
# ===
# =============================================================================


# =============================================================================
# ===
# === TEMPLATES
# ===
# =============================================================================
class AccountLoginTemplateTestCase(TestCase):

    """Log in Test Case."""

    fixtures = []

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ACCOUNTS > TEMPLATES", "green")

        # ---------------------------------------------------------------------
        # --- Fake

    def test_login_page_loading(self):
        """Docstring."""
        cprint("[---  INFO   ---] Test \"Login\" Page loading...", "cyan")

        url = reverse("login")
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True,
            secure=True)

        # print ">>> CONTEXT          :", response.context
        # print ">>> REQUEST          :", response.request
        # print ">>> STATUS           :", response.status_code
        # print ">>> TEMPLATES        :", response.templates
        # print ">>> CONTENT          :", response.content
        # print ">>> REDIRECT CHAIN   :", response.redirect_chain

        self.assertEqual(
            response.request["PATH_INFO"], url,
            "[---  ERROR  ---] Failed to load \"Login\" Page...")
        self.assertEqual(
            response.status_code, 200,
            "[---  ERROR  ---] Failed to load \"Login\" Page...")


# =============================================================================
# ===
# === FORMS
# ===
# =============================================================================


# =============================================================================
# ===
# === UTILS
# ===
# =============================================================================


"""
    self.assertEqual                /               self.assertNotEqual
    self.assertGreater
    self.assertGreaterEqual
    self.assertLess
    self.assertLessEqual
    self.assertTrue                 /               self.assertFalse
    self.assertIs                   /               self.assertIsNot
    self.assertIsNone               /               self.assertIsNotNone
    self.assertIn                   /               self.assertNotIn
    self.assertIsInstance           /               self.assertNotIsInstance
    self.assertRegexpMatches        /               self.assertNotRegexpMatches
    self.assertRaises
    self.assertRaisesRegexp

    self.assertDictContainsSubset

    self.assertContains             /               self.assertNotContains
    self.assertTemplateUsed         /               self.assertTemplateNotUsed
    self.assertInHTML
    self.assertJSONEqual            /               self.assertJSONNotEqual
"""
