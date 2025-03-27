"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.test import (
    Client,
    TestCase,
    LiveServerTestCase)


# =============================================================================
# ===
# === TEST ORGANIZATION CREATE FORM
# ===
# =============================================================================
class OrganizationCreateFormTestCase(TestCase):

    """Test Organization create Form."""

    fixtures = []

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.url = reverse("organization-organizations")
        self.login_url = reverse("signin")
        self.data = {}

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_create_event_success(self):
        """Challenge create. Success."""
        cprint("[---  INFO   ---] Test Challenge create. Success...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                "start_date":           "2017-12-31",
                "start_time":           "00:00",
                "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertTrue(
            form.is_valid())

        # self.assertEqual(form.clean_id_number(),"0000528989")
        # self.assertIn(u"Invalid Action",form.errors["__all__"])

    def test_create_event_no_avatar(self):
        """Challenge create. No Avatar."""
        cprint("[---  INFO   ---] Test Challenge create. No Avatar...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                "start_date":           "2017-12-31",
                "start_time":           "00:00",
                "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                # "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertFalse(
            form.is_valid())

    def test_create_event_no_name_no_description(self):
        """Challenge create. No Name, no Description."""
        cprint("[---  INFO   ---] Test Challenge create. No Name, no Description...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                # "name":                 "Testing Challenge #1",
                # "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                "start_date":           "2017-12-31",
                "start_time":           "00:00",
                "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertFalse(
            form.is_valid())
        self.assertIn(
            "name",
            form.errors.as_json())
        self.assertNotIn(
            "description",
            form.errors.as_json())

    def test_create_event_no_tags(self):
        """Challenge create. No Tags."""
        cprint("[---  INFO   ---] Test Challenge create. No Tags...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                # "tags":                 "testing,challenge",
                # "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                "start_date":           "2017-12-31",
                "start_time":           "00:00",
                "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertTrue(
            form.is_valid())
        self.assertNotIn(
            "tags",
            form.errors.as_json())
        self.assertNotIn(
            "hashtag",
            form.errors.as_json())

    def test_create_event_dateless(self):
        """Challenge create. Dateless."""
        cprint("[---  INFO   ---] Test Challenge create. Dateless...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Successful
        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.DATELESS,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                # "start_date":           "2017-12-31",
                # "start_time":           "00:00",
                # "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertTrue(
            form.is_valid())

        # --- Save Form
        instance = form.save()

        self.assertEqual(
            instance.recurrence,
            RECURRENCE.DATELESS)

        self.assertIn(
            MONTH.NONE,
            instance.month)
        self.assertIn(
            DAY_OF_WEEK.NONE,
            instance.day_of_week)
        self.assertIn(
            "0",
            instance.day_of_month)

        self.assertIsNone(instance.start_date)
        self.assertIsNone(instance.start_time)

        self.assertIsNotNone(instance.start_tz)

    def test_create_event_once(self):
        """Challenge create. Once. Success."""
        cprint("[---  INFO   ---] Test Challenge create. Once...", "cyan")

        # ---------------------------------------------------------------------
        # --- Log in
        result = client.login(
            username=self.test_user_1.username,
            password="test"
        )

        # ---------------------------------------------------------------------
        # --- Successful
        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                "start_date":           "2017-12-31",
                "start_time":           "00:00",
                "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertTrue(
            form.is_valid())

        # --- Save Form
        instance = form.save()

        self.assertEqual(
            instance.recurrence,
            RECURRENCE.ONCE)

        self.assertIn(
            MONTH.NONE,
            instance.month)
        self.assertIn(
            DAY_OF_WEEK.NONE,
            instance.day_of_week)
        self.assertIn(
            "0",
            instance.day_of_month)

        self.assertIsNotNone(instance.start_date)
        self.assertIsNotNone(instance.start_time)

        self.assertIsNotNone(instance.start_tz)

        # ---------------------------------------------------------------------
        # --- No Date/Time
        # ---------------------------------------------------------------------
        # --- Send Request
        form = CreateEditChallengeForm(
            data={
                "name":                 "Testing Challenge #1",
                "description":          "Description for the testing Challenge #1",
                "category":             CHALLENGE_CATEGORY.ANIMALS,
                "tags":                 "testing,challenge",
                "hashtag":              "testing-challenge",
                "duration":             8,
                "addressless":          False,
                "is_alt_person":        False,
                "contact":              "me",
                "alt_person_fullname":  "",
                "alt_person_email":     "",
                "alt_person_phone":     "",
                "recurrence":           RECURRENCE.ONCE,
                "month":                MONTH.NONE,
                "day_of_week":          DAY_OF_WEEK.NONE,
                "day_of_month":         "0",
                # "start_date":           "2017-12-31",
                # "start_time":           "00:00",
                # "start_tz":             "America/Los_Angeles",
                "organization":         None,
                "application":          CHALLENGE_MODE.FREE_FOR_ALL,
                "allow_reenter":        True,
                "accept_automatically": True,
                "acceptance_text":      "Great Job",
            },
            files={
                "avatar":               File(open("static/img/tests/challenge-test.jpg", "rb")),
            },
            user=self.test_user_1,
            )

        # ---------------------------------------------------------------------
        # --- Test Response
        form.is_valid()
        cprint("[--- ERRORS ---] %s" % form.errors.as_json(), "white", "on_red")

        self.assertFalse(
            form.is_valid())
