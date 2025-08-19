"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

import datetime
import json
import unittest
import urllib.parse

from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login)
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

from ddcore.models import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    TemporaryFile)

api_factory = APIRequestFactory()
api_client = APIClient()
client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
user_model = get_user_model()


# =============================================================================
# ===
# === ATTACHMENTS
# ===
# =============================================================================
class UploadDetailsViewSetTests(APITestCase):

    """UploadDetailsViewSet Test Class."""

    fixtures = [
        "test_accounts_users",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.tmp_file = TemporaryFile.objects.create(
            # file=request.FILES["file"],
            name="Temporary Upload",
            created_by=self.john)
        self.attached_image = AttachedImage.objects.create(
            name="Saved Image",
            # content_type=content_type,
            # object_id=object_id
            created_by=self.john)
        self.attached_document = AttachedDocument.objects.create(
            name="Saved Document",
            # content_type=content_type,
            # object_id=object_id
            created_by=self.john)
        self.attached_url = AttachedUrl.objects.create(
            url="https://2remember.live/",
            created_by=self.john)
        self.attached_video_url = AttachedVideoUrl.objects.create(
            url="https://2remember.live/",
            created_by=self.john)

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_remove_not_authenticated(self):
        """Remove Upload: User is not authenticated."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=None)
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "temp",
            "upload_id":    self.tmp_file.id,
        })
        response = api_client.delete(url, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_remove_unsupported(self):
        """Remove Upload: Unsupported Media Type."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Send Request.
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.john)
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "unsupported",
            "upload_id":    self.tmp_file.id,
        })
        response = api_client.delete(url, content_type="application/json")

        # ---------------------------------------------------------------------
        # --- Assertions.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertFalse(response.data.get("deleted"))

    def test_remove_failure(self):
        """Remove Upload: Failure."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # ---
        # --- Upload not found.
        # ---
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.john)

        # --- Temporary.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "temp",
            "upload_id":    10,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get("deleted"))

        # --- Image.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "image",
            "upload_id":    10,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get("deleted"))

        # --- Document.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "document",
            "upload_id":    10,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get("deleted"))

        # --- URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "url",
            "upload_id":    10,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get("deleted"))

        # --- Video URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "video_url",
            "upload_id":    10,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data.get("deleted"))

        # ---------------------------------------------------------------------
        # ---
        # --- User is not authorized to perform an Action.
        # ---
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.jane)

        # --- Temporary.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "temp",
            "upload_id":    self.tmp_file.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("deleted"))

        # --- Image.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "image",
            "upload_id":    self.attached_image.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("deleted"))

        # --- Document.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "document",
            "upload_id":    self.attached_document.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("deleted"))

        # --- URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "url",
            "upload_id":    self.attached_url.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("deleted"))

        # --- Video URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "video_url",
            "upload_id":    self.attached_video_url.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data.get("deleted"))

    def test_remove_success(self):
        """Remove Upload: Success."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # ---
        # --- Author.
        # ---
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.john)

        # --- Temporary.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "temp",
            "upload_id":    self.tmp_file.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("deleted"))

        # --- Image.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "image",
            "upload_id":    self.attached_image.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("deleted"))

        # --- Document.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "document",
            "upload_id":    self.attached_document.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("deleted"))

        # ---------------------------------------------------------------------
        # ---
        # --- Admin.
        # ---
        # ---------------------------------------------------------------------
        api_client.force_authenticate(user=self.admin)

        # --- URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "url",
            "upload_id":    self.attached_url.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("deleted"))

        # --- Video URL.
        url = reverse("api-upload-details", kwargs={
            "upload_type":  "video_url",
            "upload_id":    self.attached_video_url.id,
        })
        response = api_client.delete(url, content_type="application/json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data.get("deleted"))
