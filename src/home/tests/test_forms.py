"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login)
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import (
    Client,
    TestCase,
    LiveServerTestCase)

from termcolor import colored, cprint

from home.forms import (
    ContactUsForm,
    CreateEditFAQForm)
from home.models import Section


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST CONTACT US FORM
# ===
# =============================================================================
class ContactUsFormTestCase(TestCase):

    """Test Contact us Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "name":         "John Doe",
            "email":        "john.doe@gmail.com",
            "subject":      "Subject",
            "message":      "Message",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_contact_us_success_scenarios(self):
        """Contact us Success Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{}]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = ContactUsForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_contact_us_profanity_check_scenarios(self):
        """Contact us Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "name":         "sh!t",
        }, {
            "subject":      "sh!t",
        }, {
            "message":      "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = ContactUsForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_contact_us_failure_scenarios(self):
        """Contact us failed Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "name":         None,
        }, {
            "email":        None,
        }, {
            "subject":      None,
        }, {
            "message":      None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = ContactUsForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST CREATE FAQ FORM
# ===
# =============================================================================
class FAQCreateTestCase(TestCase):

    """Test create FAQ Form."""

    fixtures = [
        "test_accounts_users",
        "test_accounts_profiles",
        "test_home_faq_sections",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.section = Section.objects.first()

        self.data = {
            "question":     "Question",
            "answer":       "Answer",
            "section":      self.section,
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_faq_create_success_scenarios(self):
        """FAQ create successful Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "answer":       None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditFAQForm(
                data={
                    **self.data,
                    **scenario,
                },
                user=self.admin)
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_faq_create_profanity_check_scenarios(self):
        """FAQ create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "question":     "sh!t",
        }, {
            "answer":       "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditFAQForm(
                data={
                    **self.data,
                    **scenario,
                },
                user=self.admin)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_faq_create_failure_scenarios(self):
        """FAQ failed to create Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "question":     None,
        }, {
            "section":      None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditFAQForm(
                data={
                    **self.data,
                    **scenario,
                },
                user=self.admin)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))
