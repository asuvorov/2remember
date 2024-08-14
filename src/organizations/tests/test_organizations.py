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

from organizations.models import (
    Organization,
    OrganizationGroup,
    OrganizationStaff)


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
class OrganizationListViewTestCase(TestCase):

    """Organization List Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in                               pub Orgs

                    Logged in                               pub Orgs
                                            Auth         of prv Org
                                            Staff Member or prv Org
                                            Group Member of prv Org
                                            Auth  of Org &  Staff Member of prv Org
                                            Auth  of Org &  Group Member of prv Org
    """

    fixtures = [
        "test_accounts.json",
        "test_core_addr_acc.json",
        "test_core_addr_org.json",
        "test_organizations_private.json",
        "test_organizations_public.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > LIST", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("organization-list")

        # --- Users
        self.test_author_1 = User.objects.get(id=1)
        self.test_author_3 = User.objects.get(id=3)

        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

        # --- Organizations
        self.test_private_org_1 = Organization.objects.get(id=31)
        self.test_private_org_3 = Organization.objects.get(id=33)

        self.test_public_org_2 = Organization.objects.get(id=32)
        self.test_public_org_4 = Organization.objects.get(id=34)

    def test_user_not_logged_in(self):
        """Organization List. User NOT logged in."""
        cprint("[---  INFO   ---] Test Organization List. User NOT logged in...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))

        for organization in response.context["organizations"]:
            self.assertFalse(
                organization.is_hidden,
                colored("[---  ERROR  ---] Wrong Status of the Organization", "white", "on_red"))

    def test_user_logged_in(self):
        """Organization List. User logged in. Simple Case."""
        cprint("[---  INFO   ---] Test Organization List. User logged in. Simple Case...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
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

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))

        for organization in response.context["organizations"]:
            self.assertFalse(
                organization.is_hidden,
                colored("[---  ERROR  ---] Wrong Status of the Organization", "white", "on_red"))

    def test_user_logged_in_and_author_of_private_org(self):
        """Organization List. User logged in, and the Author of the private Organization."""
        cprint("[---  INFO   ---] Test Organization List. User logged in, and the Author of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
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

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                author=self.test_author_1,
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_staff_member_of_private_org(self):
        """Organization List. User logged in, and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization List. User logged in, and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_user_2,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                author=self.test_author_3,
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_group_member_of_private_org(self):
        """Organization List. User logged in, and the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization List. User logged in, and the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_user_2)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                id=org_group.organization.id,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_author_and_staff_member_of_private_org(self):
        """Organization List. User logged in, and Author and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization List. User logged in, and Author and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_author_1,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_author_and_group_member_of_private_org(self):
        """Organization List. User logged in, and Author the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization List. User logged in, and Author the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_author_1)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_list.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))


class OrganizationDirectoryViewTestCase(TestCase):

    """Organization Directory Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in                               pub Orgs

                    Logged in                               pub Orgs
                                            Auth         of prv Org
                                            Staff Member or prv Org
                                            Group Member of prv Org
                                            Auth  of Org &  Staff Member of prv Org
                                            Auth  of Org &  Group Member of prv Org
    """

    fixtures = [
        "test_accounts.json",
        "test_core_addr_acc.json",
        "test_core_addr_org.json",
        "test_organizations_private.json",
        "test_organizations_public.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > DIRECTORY", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("organization-directory")

        # --- Users
        self.test_author_1 = User.objects.get(id=1)
        self.test_author_3 = User.objects.get(id=3)

        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

        # --- Organizations
        self.test_private_org_1 = Organization.objects.get(id=31)
        self.test_private_org_3 = Organization.objects.get(id=33)

        self.test_public_org_2 = Organization.objects.get(id=32)
        self.test_public_org_4 = Organization.objects.get(id=34)

    def test_user_not_logged_in(self):
        """Organization Directory. User NOT logged in."""
        cprint("[---  INFO   ---] Test Organization Directory. User NOT logged in...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))

        for organization in response.context["organizations"]:
            self.assertFalse(
                organization.is_hidden,
                colored("[---  ERROR  ---] Wrong Status of the Organization", "white", "on_red"))

    def test_user_logged_in(self):
        """Organization Directory. User logged in. Simple Case."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in. Simple Case...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
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

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))

        for organization in response.context["organizations"]:
            self.assertFalse(
                organization.is_hidden,
                colored("[---  ERROR  ---] Wrong Status of the Organization", "white", "on_red"))

    def test_user_logged_in_and_author_of_private_org(self):
        """Organization Directory. User logged in, and the Author of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in, and the Author of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
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

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                author=self.test_author_1,
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_staff_member_of_private_org(self):
        """Organization Directory. User logged in, and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in, and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_user_2,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                author=self.test_author_3,
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_group_member_of_private_org(self):
        """Organization Directory. User logged in, and the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in, and the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_user_2)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                id=org_group.organization.id,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_author_and_staff_member_of_private_org(self):
        """Organization Directory. User logged in, and Author and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in, and Author and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_author_1,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))

    def test_user_logged_in_and_author_and_group_member_of_private_org(self):
        """Organization Directory. User logged in, and Author the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Directory. User logged in, and Author the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_author_1)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_directory.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            len(response.context["organizations"]),
            len(Organization.objects.filter(
                is_hidden=False,
            )) +
            len(Organization.objects.filter(
                is_hidden=True,
            )),
            colored("[---  ERROR  ---] Wrong Amount of Organizations returned", "white", "on_red"))
        self.assertIn(
            self.test_private_org_1,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))
        self.assertIn(
            self.test_private_org_3,
            response.context["organizations"],
            colored("[---  ERROR  ---] Target Organization is not returned in the List", "white", "on_red"))


class OrganizationCreateViewTestCase(TestCase):

    """Organization create Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in

                    Logged in
    """

    fixtures = [
        "test_accounts.json",
        "test_core_addr_acc.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > CREATE", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.url = reverse("organization-create")
        self.login_url = reverse("login")

        # --- Users
        self.test_user_1 = User.objects.get(id=1)
        self.test_user_3 = User.objects.get(id=3)
        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

    def test_user_not_logged_in(self):
        """Organization create. User NOT logged in."""
        cprint("[---  INFO   ---] Test Organization create. User NOT logged in...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        response = client.get(
            self.url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.login_url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_login.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        if response.redirect_chain:
            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[0]

            self.assertTrue(
                self.url in path,
                "[---  ERROR  ---] %s NOT in URL Path..." % self.url)
            self.assertEqual(
                status_code, 301,
                "[---  ERROR  ---] Wrong Status Code...")

            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[1]

            self.assertTrue(
                "?next=" in path,
                "[---  ERROR  ---] '?next=' NOT in URL Path...")
            self.assertEqual(
                status_code, 302,
                "[---  ERROR  ---] Wrong Status Code...")

    def test_user_logged_in(self):
        """Organization create. User logged in."""
        cprint("[---  INFO   ---] Test Organization create. User logged in...", "cyan")

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

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

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
            "organizations/organization_create.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))


class OrganizationDetailsViewTestCase(TestCase):

    """Organization Details Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in                               pub Org
                                                            prv Org

                    Logged in                               pub Org
                                                            prv Org
                                            Auth         of prv Org
                                            Staff Member or prv Org
                                            Group Member of prv Org
                                            Not Subscrbr of pub Org
                                                Subscrbr of pub Org
    """

    fixtures = [
        "test_accounts.json",
        "test_accounts_privacy_basic.json",
        "test_core_addr_acc.json",
        "test_core_addr_org.json",
        "test_organizations_private.json",
        "test_organizations_public.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > DETAILS", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials

        # --- Users
        self.test_author_1 = User.objects.get(id=1)
        self.test_author_3 = User.objects.get(id=3)

        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

        # --- Organizations
        self.test_private_org_1 = Organization.objects.get(id=31)
        self.test_private_org_3 = Organization.objects.get(id=33)

        self.test_public_org_2 = Organization.objects.get(id=32)
        self.test_public_org_4 = Organization.objects.get(id=34)

    def test_user_not_logged_in_public_org(self):
        """Organization Details. User NOT logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User NOT logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_public_org_2.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_2,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_not_logged_in_private_org(self):
        """Organization Details. User NOT logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User NOT logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_public_org(self):
        """Organization Details. User logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_public_org_4.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_4,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_private_org(self):
        """Organization Details. User logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_and_author_of_private_org(self):
        """Organization Details. User logged in, and the Author of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in, and the Author of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        url = reverse("organization-details", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_1,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_staff_member_of_private_org(self):
        """Organization Details. User logged in, and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in, and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_user_2,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_3,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_group_member_of_private_org(self):
        """Organization Details. User logged in, and the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in, and the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_user_2)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_3,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_not_subscriber(self):
        """Organization Details. User logged in. NOT an Organization Subscriber."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in. NOT an Organization Subscriber...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_public_org_4.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_4,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))
        self.assertFalse(
            response.context["is_subscribed"],
            colored("[---  ERROR  ---] Wrong subscribed Information returned", "white", "on_red"))

    def test_user_logged_in_subscriber(self):
        """Organization Details. User logged in. An Organization Subscriber."""
        cprint("[---  INFO   ---] Test Organization Details. User logged in. An Organization Subscriber...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Subscribed of the Organization
        self.test_public_org_4.subscribers.add(self.test_user_2)
        self.test_public_org_4.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-details", kwargs={
            "slug":     self.test_public_org_4.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_details.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_4,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))
        self.assertTrue(
            response.context["is_subscribed"],
            colored("[---  ERROR  ---] Wrong subscribed Information returned", "white", "on_red"))


class OrganizationEditViewTestCase(TestCase):

    """Organization Edit Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in                               pub Org
                                                            prv Org

                    Logged in                               pub Org
                                                            prv Org
                                            Auth         of pub Org
                                            Auth         of prv Org
                                            Staff Member or prv Org
                                            Group Member of prv Org
    """

    fixtures = [
        "test_accounts.json",
        "test_core_addr_acc.json",
        "test_core_addr_org.json",
        "test_organizations_private.json",
        "test_organizations_public.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > EDIT", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.login_url = reverse("login")

        # --- Users
        self.test_author_1 = User.objects.get(id=1)
        self.test_author_3 = User.objects.get(id=3)

        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

        # --- Organizations
        self.test_private_org_1 = Organization.objects.get(id=31)
        self.test_private_org_3 = Organization.objects.get(id=33)

        self.test_public_org_2 = Organization.objects.get(id=32)
        self.test_public_org_4 = Organization.objects.get(id=34)

    def test_user_not_logged_in_public_org(self):
        """Organization Edit. User NOT logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User NOT logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_public_org_2.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.login_url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_login.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        if response.redirect_chain:
            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[0]

            self.assertTrue(
                url in path,
                "[---  ERROR  ---] %s NOT in URL Path..." % url)
            self.assertEqual(
                status_code, 301,
                "[---  ERROR  ---] Wrong Status Code...")

            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[1]

            self.assertTrue(
                "?next=" in path,
                "[---  ERROR  ---] '?next=' NOT in URL Path...")
            self.assertEqual(
                status_code, 302,
                "[---  ERROR  ---] Wrong Status Code...")

    def test_user_not_logged_in_private_org(self):
        """Organization Edit. User NOT logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User NOT logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.login_url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_login.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        if response.redirect_chain:
            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[0]

            self.assertTrue(
                url in path,
                "[---  ERROR  ---] %s NOT in URL Path..." % url)
            self.assertEqual(
                status_code, 301,
                "[---  ERROR  ---] Wrong Status Code...")

            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[1]

            self.assertTrue(
                "?next=" in path,
                "[---  ERROR  ---] '?next=' NOT in URL Path...")
            self.assertEqual(
                status_code, 302,
                "[---  ERROR  ---] Wrong Status Code...")

    def test_user_logged_in_public_org(self):
        """Organization Edit. User logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_public_org_4.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_private_org(self):
        """Organization Edit. User logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_and_author_of_public_org(self):
        """Organization Edit. User logged in, and the Author of the public Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in, and the Author of the public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_public_org_2.slug,
            })
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_edit.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_2,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_author_of_private_org(self):
        """Organization Edit. User logged in, and the Author of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in, and the Author of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_edit.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_1,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_staff_member_of_private_org(self):
        """Organization Edit. User logged in, and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in, and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_user_2,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_edit.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_3,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_group_member_of_private_org(self):
        """Organization Edit. User logged in, and the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Edit. User logged in, and the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_user_2)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-edit", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))


class OrganizationPopulateNewsletterViewTestCase(TestCase):

    """Organization populate Newsletter Test Case.

        COVERS:
                USER                        ORGANIZATION
                --------------------------- -----------------------------------
                NOT logged in                               pub Org
                                                            prv Org

                    Logged in                               pub Org
                                                            prv Org
                                            Auth         of pub Org
                                            Auth         of prv Org
                                            Staff Member or prv Org
                                            Group Member of prv Org
    """

    fixtures = [
        "test_accounts.json",
        "test_core_addr_acc.json",
        "test_core_addr_org.json",
        "test_organizations_private.json",
        "test_organizations_public.json",
    ]

    def setUp(self):
        """Set up."""
        cprint("***" * 27, "green")
        cprint("*** TEST > ORGANIZATIONS > VIEWS > POPULATE NEWSLETTER", "green")

        # ---------------------------------------------------------------------
        # --- Fake

        # ---------------------------------------------------------------------
        # --- Initials
        self.login_url = reverse("login")

        # --- Users
        self.test_author_1 = User.objects.get(id=1)
        self.test_author_3 = User.objects.get(id=3)

        self.test_user_2 = User.objects.get(id=2)
        self.test_user_4 = User.objects.get(id=4)

        # --- Organizations
        self.test_private_org_1 = Organization.objects.get(id=31)
        self.test_private_org_3 = Organization.objects.get(id=33)

        self.test_public_org_2 = Organization.objects.get(id=32)
        self.test_public_org_4 = Organization.objects.get(id=34)

    def test_user_not_logged_in_public_org(self):
        """Organization Populate Newsletter. User NOT logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User NOT logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_public_org_2.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.login_url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_login.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        if response.redirect_chain:
            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[0]

            self.assertTrue(
                url in path,
                "[---  ERROR  ---] %s NOT in URL Path..." % url)
            self.assertEqual(
                status_code, 301,
                "[---  ERROR  ---] Wrong Status Code...")

            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[1]

            self.assertTrue(
                "?next=" in path,
                "[---  ERROR  ---] '?next=' NOT in URL Path...")
            self.assertEqual(
                status_code, 302,
                "[---  ERROR  ---] Wrong Status Code...")

    def test_user_not_logged_in_private_org(self):
        """Organization Populate Newsletter. User NOT logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User NOT logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            self.login_url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "accounts/account_login.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        if response.redirect_chain:
            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[0]

            self.assertTrue(
                url in path,
                "[---  ERROR  ---] %s NOT in URL Path..." % url)
            self.assertEqual(
                status_code, 301,
                "[---  ERROR  ---] Wrong Status Code...")

            # -----------------------------------------------------------------
            path, status_code = response.redirect_chain[1]

            self.assertTrue(
                "?next=" in path,
                "[---  ERROR  ---] '?next=' NOT in URL Path...")
            self.assertEqual(
                status_code, 302,
                "[---  ERROR  ---] Wrong Status Code...")

    def test_user_logged_in_public_org(self):
        """Organization Populate Newsletter. User logged in. Public Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in. Public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_public_org_4.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_private_org(self):
        """Organization Populate Newsletter. User logged in. Private Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in. Private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

    def test_user_logged_in_and_author_of_public_org(self):
        """Organization Populate Newsletter. User logged in, and the Author of the public Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in, and the Author of the public Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_public_org_2.slug,
            })
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_populate_newsletter.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_public_org_2,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_author_of_private_org(self):
        """Organization Populate Newsletter. User logged in, and the Author of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in, and the Author of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_author_1.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Send Request
        data = {}
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_private_org_1.slug,
            })
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_populate_newsletter.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_1,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_staff_member_of_private_org(self):
        """Organization Populate Newsletter. User logged in, and the Staff Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in, and the Staff Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Staff Member of the private Organization
        OrganizationStaff.objects.create(
            author=self.test_author_3,
            organization=self.test_private_org_3,
            member=self.test_user_2,
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            200,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "organizations/organization_populate_newsletter.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))

        self.assertEqual(
            response.context["organization"],
            self.test_private_org_3,
            colored("[---  ERROR  ---] Wrong Organization returned", "white", "on_red"))

    def test_user_logged_in_and_group_member_of_private_org(self):
        """Organization Populate Newsletter. User logged in, and the Group Member of the private Organization."""
        cprint("[---  INFO   ---] Test Organization Populate Newsletter. User logged in, and the Group Member of the private Organization...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_2.username,
            password="test"
        )
        # cprint("[---  DUMP   ---] LOGIN            : %s" % result, "yellow")

        # ---------------------------------------------------------------------
        # --- Make User a Group Member of the private Organization
        org_group = OrganizationGroup.objects.create(
            author=self.test_author_3,
            name="Test Group",
            organization=self.test_private_org_3,
        )
        org_group.members.add(self.test_user_2)
        org_group.save()

        # ---------------------------------------------------------------------
        # --- Send Request
        url = reverse("organization-populate-newsletter", kwargs={
            "slug":     self.test_private_org_3.slug,
            })
        data = {}
        response = client.get(
            url,
            data=data,
            follow=True)

        cprint(f"[---  DUMP   ---] CONTEXT          : {response.context["organizations"]}", "yellow")
        cprint(f"[---  DUMP   ---] REQUEST          : {response.request}", "yellow")
        cprint(f"[---  DUMP   ---] STATUS           : {response.status_code}", "yellow")
        cprint(f"[---  DUMP   ---] TEMPLATES        : {response.templates}", "yellow")
        cprint(f"[---  DUMP   ---] CONTENT          : {response.content}", "yellow")
        cprint(f"[---  DUMP   ---] REDIRECT CHAIN   : {response.redirect_chain}", "yellow")

        # ---------------------------------------------------------------------
        # --- Test Response
        self.assertEqual(
            response.request["PATH_INFO"],
            url,
            colored("[---  ERROR  ---] Wrong Path", "white", "on_red"))
        self.assertEqual(
            response.status_code,
            404,
            colored("[---  ERROR  ---] Wrong Status Code", "white", "on_red"))
        self.assertTemplateUsed(
            response,
            "404.html",
            colored("[---  ERROR  ---] Wrong Template used", "white", "on_red"))


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
