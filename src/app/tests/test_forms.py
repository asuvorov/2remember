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

from ddcore.models import (
    GenderType,
    PhoneType,
    SocialApp)

from app.forms import (
    AddressForm,
    PhoneForm,
    CreateNewsletterForm,
    SocialLinkForm)


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST ADDRESS FORM
# ===
# =============================================================================
class AddressFormTestCase(TestCase):

    """Test Address Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "address_1":    "111 Main Str.",
            "address_2":    None,
            "city":         "Palm Springs",
            "zip_code":     "90000",
            "province":     "CA",
            "country":      "US",
            "notes":        None,
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_address_create_success(self):
        """Address successfully created."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = AddressForm(
            data=self.data,
            required=True)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = AddressForm(
            data={
                **self.data,
                "address_1":    None,
                "city":         None,
                "zip_code":     None,
                # "country":      None,  # FIXME: Should work.
            },
            required=False)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_address_success_scenarios(self):
        """Address successfully created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [
            (None, "US"),
            # ("CA", "CA"),
            ("XX", "US"),
        ]
        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = AddressForm(
                data=self.data,
                country_code=scenario[0])

            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))
            self.assertEqual(form.cleaned_data["country"], scenario[1], msg=colored(scenario[0], "white", "on_red"))

    def test_address_create_profanity_check_scenarios(self):
        """Address create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "address_1":    "sh!t",
        }, {
            "address_2":    "sh!t",
        }, {
            "city":         "sh!t",
        }, {
            "zip_code":     "sh!t",
        }, {
            "province":     "sh!t",
        }, {
            "notes":        "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = AddressForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_address_create_failure_scenarios(self):
        """Address failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "address_1":    None,
        }, {
            "city":         None,
        }, {
            "zip_code":     None,
        }, {
            "country":      None,
        }, {
            "country":      "XX",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = AddressForm(
                data={
                    **self.data,
                    **scenario,
                },
                required=True)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST PHONE FORM
# ===
# =============================================================================
class PhoneFormTestCase(TestCase):

    """Test Phone Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "phone_number":     "+12345678910",
            "phone_number_ext": None,
            "phone_type":       PhoneType.MOBILE,
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_phone_create_success(self):
        """Phone successfully created."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = PhoneForm(
            data=self.data,
            required=True)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = PhoneForm(
            data={
                **self.data,
                "phone_number":     None,
                "phone_number_ext": None,
                "phone_type":       None,
            },
            required=False)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_phone_success_scenarios(self):
        """Phone successfully created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "phone_number_ext": None
        }, {
            "phone_type":       None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = PhoneForm(
                data={
                    **self.data,
                    **scenario,
                })

            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_phone_create_failure_scenarios(self):
        """Phone failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "phone_number":     None,
        }, {
            "phone_number_ext": "1234567890",  # Too long.
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = PhoneForm(
                data={
                    **self.data,
                    **scenario,
                },
                required=True)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST NEWSLETTER CREATE FORM
# ===
# =============================================================================
class NewsletterCreateFormTestCase(TestCase):

    """Test Newsletter create Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "title":        "Newsletter Title",
            "content":      "Newsletter Content",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_newsletter_create_success(self):
        """Newsletter successfully created."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = CreateNewsletterForm(data=self.data)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_newsletter_create_profanity_check_scenarios(self):
        """Newsletter create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "title":        "sh!t",
        }, {
            "content":      "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateNewsletterForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_newsletter_create_failure_scenarios(self):
        """Newsletter failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "title":        None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateNewsletterForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST SOCIAL LINK FORM
# ===
# =============================================================================
class SocialLinkFormTestCase(TestCase):

    """Test Social Link Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "social_app":   SocialApp.FACEBOOK,
            "url":          "https://facebook.com",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_social_link_create_success(self):
        """Social Link successfully created."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        form = SocialLinkForm(data=self.data)

        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_social_link_success_scenarios(self):
        """Social Link successfully created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "social_app":   SocialApp.FACEBOOK,
        }, {
            "url":          None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = SocialLinkForm(
                data={
                    **self.data,
                    **scenario,
                })

            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_social_link_create_failure_scenarios(self):
        """Social Link failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "social_app":   None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = SocialLinkForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))
