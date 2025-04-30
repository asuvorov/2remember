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

from app.models import Visibility
from events.forms import CreateEditEventForm


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST EVENT CREATE FORM
# ===
# =============================================================================
class EventCreateFormTestCase(TestCase):

    """Test Event create Form."""

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

        self.data = {
            "title":            "Testing Event",
            "description":      "Description for the testing Event",
            "category":         None,
            "visibility":       Visibility.PUBLIC,
            "tags":             "testing,event",
            "hashtag":          "testing-event",
            "addressless":      False,
            "organization":     None,
            "allow_comments":   True,
        }
        self.files = {
            "preview":  SimpleUploadedFile(
                            "challenge-test.jpg",
                            File(open(finders.find("tests/challenge-test.jpg"), "rb")).read(),
                            content_type="multipart/form-data"),
            "cover":    SimpleUploadedFile(
                            "challenge-test.jpg",
                            File(open(finders.find("tests/challenge-test.jpg"), "rb")).read(),
                            content_type="multipart/form-data")
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_event_create_success_no_avatars(self):
        """Event successfully created: No Avatars."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = CreateEditEventForm(
            data=self.data,
            files={},
            user=self.admin)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_event_create_success_scenarios(self):
        """Event successfully created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "description":  None,
        }, {
            "visibility":   Visibility.PRIVATE,
        }, {
            "tags":         None,
        }, {
            "hashtag":      None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditEventForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_event_create_success_tags_scenarios(self):
        """Event successfully created: Tags Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [
            ("apple ball cat", ["apple ball cat"]),                     # No Commas, so Space-delimited.
            ("apple, ball cat", ["apple", "ball cat"]),                 # Comma present, so Comma-delimited.
            ("\"apple, ball\" cat dog", ["apple, ball", "cat", "dog"]), # All Commas are quoted, so Space-delimited.
            ("\"apple, ball\", cat dog", ["apple, ball", "cat dog"]),   # Contains an unquoted Comma, so Comma-delimited.
            ("apple \"ball cat\" dog", ["apple", "ball cat", "dog"]),   # No Commas, so Space-delimited.
            ("\"apple\" \"ball dog", ["apple ball dog"]),               # Unclosed double Quote is ignored.
            ("\"apple ball cat\"", ["apple ball cat"]),
        ]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditEventForm(
                data={
                    **self.data,
                    "tags":     scenario[0],
                },
                files=self.files,
                user=self.admin)
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))
            self.assertCountEqual(form.cleaned_data["tags"], scenario[1], msg=colored(scenario[0], "white", "on_red"))

    def test_event_create_profanity_check_scenarios(self):
        """Event create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "title":        "sh!t",
        }, {
            "description":  "sh!t",
        }, {
            "tags":         "sh!t",
        }, {
            "hashtag":      "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditEventForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertTrue(form.is_valid(), msg=colored(scenario, "white", "on_red"))

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditEventForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.john)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_event_create_failure_scenarios(self):
        """Event failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "title":        None,
        }, {
            "visibility":   None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = CreateEditEventForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))
