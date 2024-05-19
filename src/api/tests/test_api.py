"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import datetime
import json
import unittest
import urllib.parse

from django.conf import settings
from django.contrib.auth import authenticate, login
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


api_factory = APIRequestFactory()
api_client = APIClient()
client = Client(
    HTTP_USER_AGENT="Mozilla/5.0",
    enforce_csrf_checks=True)
