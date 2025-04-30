"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import uuid

# from django.contrib.auth import (
#     authenticate,
#     get_user_model,
#     login)
from django.test import TestCase
from django.test.client import RequestFactory


class GenericUserTestCase(TestCase):
    """Generic User Model Test Class."""

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.ip = "127.0.0.1"
        self.user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36")
        self.provider = "Cox"
        self.geo_data = {
            "country_code":     "XX",
            "country_name":     "unknown",
            "remote_addr":      "127.0.0.1",
        }

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def _generate_post_request(self, user=None, headers=None, data=None):
        """Generate POST Request."""
        rf = RequestFactory(headers=headers) if isinstance(headers, dict) else RequestFactory()
        request = rf.post("/singin/", data if isinstance(data, dict) else {})
        setattr(request, "user", user)
        setattr(request, "geo_data", self.geo_data)
        setattr(request, "request_id", f"{uuid.uuid4()}")

        return request
