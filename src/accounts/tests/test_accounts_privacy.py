"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

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


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ MOCKS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ AJAX
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ API
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class AutocompleteMemberViewTestCase(APITestCase):

    """API: Autocomplete Members List Test Case."""

    fixtures = [
        "test_accounts_users.json",
        "test_accounts_profiles.json",
        "test_accounts_privacy_basic.json",
        "test_core_addresses_accounts.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("autocomplete-member-list")

        # --- Users
        self.test_user_admin = User.objects.get(id=1)
        self.test_user_john = User.objects.get(id=2)
        self.test_user_artem = User.objects.get(id=3)
        self.test_user_maryna = User.objects.get(id=4)

        # ---------------------------------------------------------------------
        # --- Get or create API Auth Token
        self.token, created = Token.objects.get_or_create(
            user=self.test_user_admin,
            )

    def test_10_user_not_logged_in(self):
        """API. User NOT logged in."""
        cprint("[---  INFO   ---] Test API. User NOT logged in..", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {
            "term":     "art",
        }
        response = api_client.get(
            path=self.url,
            data=data,
            format="json")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
            colored("[---  ERROR  ---] Wrong Status Code <%s>" % response.status_code, "white", "on_red"))

    def test_21_member_appears_in_autocomplete(self):
        """API. Member appears in the Autocomplete Members List."""
        cprint("[---  INFO   ---] Test API. Member appears in the Autocomplete Members List...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        # api_client.credentials(
        #     HTTP_AUTHORIZATION="Token %s" % self.token.key)
        result = api_client.login(
            username=self.test_user_admin.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {
            "term":     "art",
        }
        response = api_client.get(
            path=self.url,
            data=data,
            format="json")

        cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context, "yellow")
        cprint("[---  DUMP   ---] REQUEST          : %s" % response.request, "yellow")
        cprint("[---  DUMP   ---] STATUS           : %s" % response.status_code, "yellow")
        cprint("[---  DUMP   ---] TEMPLATES        : %s" % response.templates, "yellow")
        cprint("[---  DUMP   ---] CONTENT          : %s" % response.content, "yellow")
        # cprint("[---  DUMP   ---] REDIRECT CHAIN   : %s" % response.redirect_chain, "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            colored("[---  ERROR  ---] Wrong Status Code <%s>" % response.status_code, "white", "on_red"))

        self.assertEqual(
            len(response.context["accounts"]),
            len(User.objects.filter(
                is_active=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))

    def test_22_member_not_appears_in_autocomplete(self):
        """API. Member NOT appears in the Autocomplete Members List."""
        cprint("[---  INFO   ---] Test API. Member NOT appears in the Autocomplete Members List...", "cyan")

        # ---------------------------------------------------------------------
        # --- Initials
        self.test_user_artem.privacy_general.hide_profile_from_search = True
        self.test_user_artem.privacy_general.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {
            "term":     "art",
        }
        api_client.credentials(
            HTTP_AUTHORIZATION="Token %s" % self.token.key)
        response = api_client.get(
            path=self.url,
            data=data,
            format="json")

        cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context, "yellow")
        cprint("[---  DUMP   ---] REQUEST          : %s" % response.request, "yellow")
        cprint("[---  DUMP   ---] STATUS           : %s" % response.status_code, "yellow")
        cprint("[---  DUMP   ---] TEMPLATES        : %s" % response.templates, "yellow")
        cprint("[---  DUMP   ---] CONTENT          : %s" % response.content, "yellow")
        # cprint("[---  DUMP   ---] REDIRECT CHAIN   : %s" % response.redirect_chain, "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            colored("[---  ERROR  ---] Wrong Status Code <%s>" % response.status_code, "white", "on_red"))

        self.assertEqual(
            len(response.context["accounts"]),
            len(User.objects.filter(
                is_active=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ FORMS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ MODELS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ UTILS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ VIEWS
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("account-list")

        # --- Users
        self.test_user_admin = User.objects.get(id=1)
        self.test_user_john = User.objects.get(id=2)
        self.test_user_artem = User.objects.get(id=3)
        self.test_user_maryna = User.objects.get(id=4)

    def test_10_member_appears_in_account_list(self):
        """Account List. Member appears in the Account List."""
        cprint("[---  INFO   ---] Test Account List. Member appears in the Account List...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_admin.username,
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

        # cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context, "yellow")
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
            status.HTTP_200_OK,
            colored("[---  ERROR  ---] Wrong Status Code <%s>" % response.status_code, "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertTrue(
            self.test_user_artem in response.context["accounts"],
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))

    def test_11_member_not_appears_in_account_list(self):
        """Account List. Member NOT appears in the Account List."""
        cprint("[---  INFO   ---] Test Account List. Member NOT appears in the Account List...", "cyan")

        # ---------------------------------------------------------------------
        # --- Initials
        self.test_user_artem.privacy_general.hide_profile_from_list = True
        self.test_user_artem.privacy_general.save()

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_admin.username,
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

        # cprint("[---  DUMP   ---] CONTEXT          : %s" % response.context, "yellow")
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
            status.HTTP_200_OK,
            colored("[---  ERROR  ---] Wrong Status Code <%s>" % response.status_code, "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertTrue(
            self.test_user_artem not in response.context["accounts"],
            colored("[---  ERROR  ---] Wrong Amount of Accounts returned", "white", "on_red"))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~
# ~~~ TEMPLATES
# ~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


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
