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

from ddcore.models import GenderType

from accounts.forms import (
    LoginForm,
    UserForm,
    UserProfileForm,
    UserProfileEditForm,
    ForgotPasswordForm,
    ResetPasswordForm)


client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === TEST USER LOGIN FORM
# ===
# =============================================================================
class UserLoginFormTestCase(TestCase):

    """Test User login Form."""

    fixtures = [
        "test_accounts_users",
        "test_accounts_profiles",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "username":     "admin",
            "password":     "admin",
            "remember_me":  True,
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_login_user_success(self):
        """User successfully logged in."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = LoginForm(data=self.data)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_login_user_failure_scenarios(self):
        """User failed to login Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "username":     None,
        }, {
            "password":     None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = LoginForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST USER FORM
# ===
# =============================================================================
class UserFormTestCase(TestCase):

    """Test User Form."""

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
            "first_name":   "admin",
            "last_name":    "admin",
            "email":        "admin@google.com",
            "password":     "Admin_1",
            "retry":        "Admin_1",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_user_create_success(self):
        """User successfully created."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = UserForm(data=self.data)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_user_create_profanity_check_scenarios(self):
        """User create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "first_name":   "sh!t",
        }, {
            "last_name":    "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_user_create_failure_scenarios(self):
        """User failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "first_name":   None,
        }, {
            "last_name":    None,
        }, {
            "email":        None,
        }, {
            "email":        self.admin.email,  # Email of an existing User.
        }, {
            "password":     None,
        }, {
            "password":     "short",
        }, {
            "retry":        None,
        }, {
            "password":     "admin",
            "retry":        "user",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST USER PROFILE FORM
# ===
# =============================================================================
class UserProfileFormTestCase(TestCase):

    """Test User Profile Form."""

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
            "nickname":             "admin",
            "bio":                  "bio",
            "gender":               GenderType.OTHER,
            "birth_day":            "1984-05-14",
            "allow_comments":       True,
            "receive_newsletters":  True,
        }
        self.files = {
            "avatar":   SimpleUploadedFile(
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

    def test_user_profile_success_no_avatars(self):
        """User Profile successfully created: No Avatars."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = UserProfileForm(
            data=self.data,
            files={})

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_user_profile_success_scenarios(self):
        """User Profile successfully created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "nickname":     None,
        }, {
            "bio":          None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files)
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_user_profile_profanity_check_scenarios(self):
        """User Profile create Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "nickname":     "sh!t",
        }, {
            "bio":          "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_user_profile_failure_scenarios(self):
        """User Profile failed to be created Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "gender":       None,
        }, {
            "birth_day":    None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST USER PROFILE EDIT FORM
# ===
# =============================================================================
class UserProfileEditFormTestCase(TestCase):

    """Test User Profile Edit Form."""

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
            "first_name":           "admin",
            "last_name":            "admin",
            "email":                "admin@google.com",
            "nickname":             "admin",
            "bio":                  "bio",
            "gender":               GenderType.OTHER,
            "birth_day":            "1984-05-14",
            "allow_comments":       True,
            "receive_newsletters":  True,
        }
        self.files = {
            "avatar":   SimpleUploadedFile(
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

    def test_user_profile_edit_success_no_avatars(self):
        """User Profile successfully edited: No Avatars."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = UserProfileEditForm(
            data=self.data,
            files={},
            user=self.admin)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_user_profile_edit_success_scenarios(self):
        """User Profile successfully edited Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "first_name":   "Thomas",
        }, {
            "last_name":    "Jefferson",
        }, {
            "email":        "thomas@gmail.com",
        }, {
            "nickname":     None,
        }, {
            "bio":          None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileEditForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_user_profile_edit_profanity_check_scenarios(self):
        """User Profile edit Profanity Check."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "first_name":   "sh!t",
        }, {
            "last_name":    "sh!t",
        }, {
            "nickname":     "sh!t",
        }, {
            "bio":          "sh!t",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileEditForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))

    def test_user_profile_edit_failure_scenarios(self):
        """User Profile failed to be edited Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "first_name":   None,
        }, {
            "last_name":    None,
        }, {
            "email":        None,
        }, {
            "gender":       None,
        }, {
            "birth_day":    None,
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = UserProfileEditForm(
                data={
                    **self.data,
                    **scenario,
                },
                files=self.files,
                user=self.admin)
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST FORGOT PASSWORD FORM
# ===
# =============================================================================
class ForgotPasswordFormTestCase(TestCase):

    """Test forgot Password Form."""

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
            "email":        self.admin.email,
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_forgot_password_success(self):
        """Forgot Password Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = ForgotPasswordForm(data=self.data)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_forgot_password_failure_scenarios(self):
        """Forgot Password Failure Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "email":        None,
        }, {
            "email":        "admin@google.com",  # Email of non-existing User.
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = ForgotPasswordForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST USER FORM
# ===
# =============================================================================
class ResetPasswordFormFormTestCase(TestCase):

    """Test reset Password Form."""

    fixtures = [
        "test_accounts_users",
        "test_accounts_profiles",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.data = {
            "password":     "Admin_1",
            "retry":        "Admin_1",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_reset_password_success(self):
        """Reset Password Success."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        form = ResetPasswordForm(data=self.data)

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

    def test_reset_password_failure_scenarios(self):
        """Reset Password Failure Scenarios."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        scenarios = [{
            "password":     None,
        }, {
            "password":     "short",
        }, {
            "retry":        None,
        }, {
            "password":     "admin",
            "retry":        "user",
        }]

        # ---------------------------------------------------------------------
        # --- Prepare and send Request, and test Response.
        # ---------------------------------------------------------------------
        for scenario in scenarios:
            form = ResetPasswordForm(
                data={
                    **self.data,
                    **scenario,
                })
            self.assertFalse(form.is_valid(), msg=colored(scenario, "white", "on_red"))


# =============================================================================
# ===
# === TEST USER PROFILE FORM
# ===
# =============================================================================
# class UserProfileFormTestCase(TestCase):

#     """Test User Profile Form."""

#     fixtures = [
#         "test_accounts_users",
#         "test_accounts_profiles",
#     ]

#     def setUp(self):
#         """Constructor."""
#         super().setUp()

#         self.admin = user_model.objects.get(username="admin")
#         self.john = user_model.objects.get(username="john")
#         self.jane = user_model.objects.get(username="jane")

#         self.data = {
#             "title":            "Testing Event",
#             "description":      "Description for the testing Event",
#             "category":         None,
#             "visibility":       Visibility.PUBLIC,
#             "tags":             "testing,event",
#             "hashtag":          "testing-event",
#             "addressless":      False,
#             "organization":     None,
#             "allow_comments":   True,
#         }
#         self.files = {
#             "preview":  SimpleUploadedFile(
#                             "challenge-test.jpg",
#                             File(open(finders.find("tests/challenge-test.jpg"), "rb")).read(),
#                             content_type="multipart/form-data"),
#             "cover":    SimpleUploadedFile(
#                             "challenge-test.jpg",
#                             File(open(finders.find("tests/challenge-test.jpg"), "rb")).read(),
#                             content_type="multipart/form-data")
#         }

#     def tearDown(self):
#         """Destructor."""
#         super().tearDown()

#     def test_create_event_success_no_avatars(self):
#         """Event successfully created: No Avatars."""
#         # ---------------------------------------------------------------------
#         # --- Initials.
#         # ---------------------------------------------------------------------

#         # ---------------------------------------------------------------------
#         # --- Prepare and send Request.
#         # ---------------------------------------------------------------------
#         form = CreateEditEventForm(
#             data=self.data,
#             files={},
#             user=self.admin)

#         # ---------------------------------------------------------------------
#         # --- Test Response.
#         # ---------------------------------------------------------------------
#         self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

#     def test_create_event_success_scenarios(self):
#         """Event successfully created Scenarios."""
#         # ---------------------------------------------------------------------
#         # --- Initials.
#         # ---------------------------------------------------------------------
#         scenarios = [{
#             "description":  None,
#         }, {
#             "visibility":   Visibility.PRIVATE,
#         }, {
#             "tags":         None,
#         }, {
#             "hashtag":      None,
#         }]

#         # ---------------------------------------------------------------------
#         # --- Prepare and send Request, and test Response.
#         # ---------------------------------------------------------------------
#         for scenario in scenarios:
#             form = CreateEditEventForm(
#                 data={
#                     **self.data,
#                 },
#                 files=self.files,
#                 user=self.admin)
#             self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))

#     def test_create_event_success_tags_scenarios(self):
#         """Event successfully created: Tags Scenarios."""
#         # ---------------------------------------------------------------------
#         # --- Initials.
#         # ---------------------------------------------------------------------
#         scenarios = [
#             ("apple ball cat", ["apple ball cat"]),                     # No Commas, so Space-delimited.
#             ("apple, ball cat", ["apple", "ball cat"]),                 # Comma present, so Comma-delimited.
#             ("\"apple, ball\" cat dog", ["apple, ball", "cat", "dog"]), # All Commas are quoted, so Space-delimited.
#             ("\"apple, ball\", cat dog", ["apple, ball", "cat dog"]),   # Contains an unquoted Comma, so Comma-delimited.
#             ("apple \"ball cat\" dog", ["apple", "ball cat", "dog"]),   # No Commas, so Space-delimited.
#             ("\"apple\" \"ball dog", ["apple ball dog"]),               # Unclosed double Quote is ignored.
#             ("\"apple ball cat\"", ["apple ball cat"]),
#         ]

#         # ---------------------------------------------------------------------
#         # --- Prepare and send Request, and test Response.
#         # ---------------------------------------------------------------------
#         for scenario in scenarios:
#             form = CreateEditEventForm(
#                 data={
#                     **self.data,
#                     "tags":     scenario[0],
#                 },
#                 files={},
#                 user=self.admin)
#             self.assertTrue(form.is_valid(), msg=colored(form.errors, "white", "on_red"))
#             self.assertCountEqual(form.cleaned_data["tags"], scenario[1], msg=colored(scenario[0], "white", "on_red"))

#     def test_create_event_failure_scenarios(self):
#         """Event failed to be created Scenarios."""
#         # ---------------------------------------------------------------------
#         # --- Initials.
#         # ---------------------------------------------------------------------
#         scenarios = [{
#             "title":        None,
#         }, {
#             "visibility":   None,
#         }]

#         # ---------------------------------------------------------------------
#         # --- Prepare and send Request, and test Response.
#         # ---------------------------------------------------------------------
#         for scenario in scenarios:
#             form = CreateEditEventForm(
#                 data={
#                     **self.data,
#                     **scenario,
#                 },
#                 files={},
#                 user=self.admin)
#             self.assertFalse(form.is_valid())
