"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import http.client
import pytest

from django.test import TestCase
from django.test.client import RequestFactory

from rest_framework.test import APIClient

from events.models import (
    Event,
    Visibility)
from tests.test_core import GenericUserTestCase


# =============================================================================
# ===
# === TEST PRIVATE EVENTS.
# ===
# =============================================================================
class PrivateEventTestCase(GenericUserTestCase):
    """Test private Events."""

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.event = Event.objects.create(
            author=self.admin,
            title="Private Event",
            visibility=Visibility.PRIVATE)

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
