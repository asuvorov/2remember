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
from django.contrib.staticfiles import finders
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
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
class TmpUploadViewSetTests(APITestCase):

    """TmpUploadViewSet Test Class."""

    fixtures = [
        "test_accounts_users",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.url = reverse("api-tmp-upload")
        self.data = {}

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.test_file_unsupported = SimpleUploadedFile(
            "unsupported.geo",
            File(open(finders.find("tests/unsupported.geo"), "rb")).read(),
            content_type="multipart/form-data")

        self.test_file_img_small = SimpleUploadedFile(
            "img_small.jpg",
            File(open(finders.find("tests/img_small.jpg"), "rb")).read(),
            content_type="multipart/form-data")
        self.test_file_img_big = SimpleUploadedFile(
            "img_big.jpg",
            File(open(finders.find("tests/img_big.jpg"), "rb")).read(),
            content_type="multipart/form-data")

        self.test_file_doc_small = SimpleUploadedFile(
            "doc_small.txt",
            File(open(finders.find("tests/doc_small.txt"), "rb")).read(),
            content_type="multipart/form-data")
        self.test_file_doc_big = SimpleUploadedFile(
            "doc_big.txt",
            File(open(finders.find("tests/doc_big.txt"), "rb")).read(),
            content_type="multipart/form-data")

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Temporary Upload: User is not authorized."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, data={}, format="json")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_files(self):
        """Temporary Upload: User has not provided the File(s) in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data={}, format="json")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_unsupported_file(self):
        """Temporary Upload: User provides the File(s) of unsupported Format in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = {
            "file": self.test_file_unsupported,
        }

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data, format="multipart")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        self.assertTrue(isinstance(response.data["files"], list))
        self.assertEqual(len(response.data["files"]), 0)

    def test_upload_img(self):
        """Temporary Upload: User provides the Image File(s) in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data_small = {
            "file": self.test_file_img_small,
        }
        data_big = {
            "file": self.test_file_img_big,
        }

        # ---------------------------------------------------------------------
        # --- User provides the Image File(s) of allowed Size in Request.
        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_small, format="multipart")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data["files"], list))
        self.assertEqual(len(response.data["files"]), 1)

        # ---------------------------------------------------------------------
        # --- User provides the Image File(s) of excessive Size in Request.
        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_big, format="multipart")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        self.assertTrue(isinstance(response.data["files"], list))
        self.assertEqual(len(response.data["files"]), 0)

    def test_upload_doc(self):
        """Temporary Upload: User provides the Document File(s) in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data_small = {
            "file": self.test_file_doc_small,
        }
        data_big = {
            "file": self.test_file_doc_big,
        }

        # ---------------------------------------------------------------------
        # --- User provides the Document File(s) of allowed Size in Request.
        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_small, format="multipart")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data["files"], list))
        self.assertEqual(len(response.data["files"]), 1)

        # ---------------------------------------------------------------------
        # --- User provides the Document File(s) of excessive Size in Request.
        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_big, format="multipart")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
        self.assertTrue(isinstance(response.data["files"], list))
        self.assertEqual(len(response.data["files"]), 0)


class RemoveUploadViewSetTests(APITestCase):

    """RemoveUploadViewSet Test Class."""

    fixtures = [
        "test_accounts_users",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.url = reverse("api-remove-upload")
        self.data = {}

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

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Remove Upload: User is not authorized."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = {
            "type":     "document",
            "id":       1
        }

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, data, format="json")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_payload(self):
        """Remove Upload: User has not provided sufficient Payload in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)

        data_upload_type = {
            "type":     "temp",
        }
        data_upload_id = {
            "id":       1,
        }

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_type, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_id, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

    def test_upload_doesnot_exist(self):
        """Remove Upload: Upload does not exist."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)

        data_upload_nil = {
            "type":     "unsupported",
            "id":       1000,
        }
        data_upload_doc = {
            "type":     "document",
            "id":       1000,
        }
        data_upload_img = {
            "type":     "image",
            "id":       1000,
        }
        data_upload_tmp = {
            "type":     "temp",
            "id":       1000,
        }

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_nil, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_doc, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_img, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_upload_tmp, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

    def test_upload_exists(self):
        """Remove Upload: Upload exists."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data_upload_doc = {
            "type":     "document",
            "id":       self.attached_document.id,
        }
        data_upload_img = {
            "type":     "image",
            "id":       self.attached_image.id,
        }
        data_upload_tmp = {
            "type":     "temp",
            "id":       self.tmp_file.id,
        }

        # ---------------------------------------------------------------------
        # --- Non-Author tries to delete the Upload.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.jane)
        response = self.client.post(self.url, data_upload_tmp, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Author tries to delete the Upload.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_upload_doc, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Admin tries to delete the Upload.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, data_upload_img, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["deleted"])


class RemoveLinkViewSetTests(APITestCase):

    """RemoveLinkViewSet Test Class."""

    fixtures = [
        "test_accounts_users",
    ]

    def setUp(self):
        """Constructor."""
        super().setUp()

        self.url = reverse("api-remove-link")
        self.data = {}

        self.admin = user_model.objects.get(username="admin")
        self.john = user_model.objects.get(username="john")
        self.jane = user_model.objects.get(username="jane")

        self.attached_url = AttachedUrl.objects.create(
            url="https://2remember.live/",
            created_by=self.john)
        self.attached_video_url = AttachedVideoUrl.objects.create(
            url="https://2remember.live/",
            created_by=self.john)

    def tearDown(self):
        """Destructor."""
        super().tearDown()

    def test_unauthorized(self):
        """Remove Link: User is not authorized."""

        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data = {
            "type":     "regular",
            "id":       1
        }

        # ---------------------------------------------------------------------
        # --- Prepare and send Request.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, data, format="json")

        # ---------------------------------------------------------------------
        # --- Test Response.
        # ---------------------------------------------------------------------
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_no_payload(self):
        """Remove Link: User has not provided sufficient Payload in Request."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)

        data_link_type = {
            "type":     "regular",
        }
        data_link_id = {
            "id":       1,
        }

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, self.data, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_link_type, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_link_id, format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["deleted"])

    def test_link_doesnot_exist(self):
        """Remove Link: Link does not exist."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)

        data_link_nil = {
            "type":     "unsupported",
            "id":       1000,
        }
        data_link_regular = {
            "type":     "regular",
            "id":       1000,
        }
        data_link_video = {
            "type":     "video",
            "id":       1000,
        }

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_link_nil, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_link_regular, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        response = self.client.post(self.url, data_link_video, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

    def test_link_exists(self):
        """Remove Link: Link exists."""
        # ---------------------------------------------------------------------
        # --- Initials.
        # ---------------------------------------------------------------------
        data_link_regular = {
            "type":     "regular",
            "id":       self.attached_url.id,
        }
        data_link_video = {
            "type":     "video",
            "id":       self.attached_video_url.id,
        }

        # ---------------------------------------------------------------------
        # --- Non-Author tries to delete the Link.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.jane)
        response = self.client.post(self.url, data_link_regular, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Author tries to delete the Link.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.john)
        response = self.client.post(self.url, data_link_regular, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["deleted"])

        # ---------------------------------------------------------------------
        # --- Admin tries to delete the Link.
        # ---------------------------------------------------------------------
        # --- Send Request, and test Response.
        # ---------------------------------------------------------------------
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.url, data_link_video, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["deleted"])
