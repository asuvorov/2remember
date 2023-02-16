import datetime
import http.client

from django.test import TestCase
from django.utils import timezone

from invites.models import Invite


class RobotsTest(TestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        self.assertEqual(response.status_code, http.client.OK)
        self.assertEqual(response["content-type"], "text/plain")

    def test_post(self):
        response = self.client.post("/robots.txt")

        self.assertEqual(response.status_code, http.client.METHOD_NOT_ALLOWED)


class HumansTest(TestCase):
    def test_get(self):
        response = self.client.get("/humans.txt")

        self.assertEqual(response.status_code, http.client.OK)
        self.assertEqual(response["content-type"], "text/plain")

    def test_post(self):
        response = self.client.post("/humans.txt")

        self.assertEqual(response.status_code, http.client.METHOD_NOT_ALLOWED)
