"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from decouple import config

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *


# -----------------------------------------------------------------------------
# --- Override Settings here.
# -----------------------------------------------------------------------------
DEBUG = True

# SECRET_KEY = config("SECRET_KEY", default="")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)


###############################################################################
### AWS SETTINGS                                                            ###
###############################################################################
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_S3_BUCKET = config("AWS_S3_BUCKET", default="")
AWS_PRELOAD_METADATA = config("AWS_PRELOAD_METADATA", default=True, cast=bool)
AWS_QUERYSTRING_AUTH = config("AWS_QUERYSTRING_AUTH", default=False, cast=bool)
AWS_HEADERS = {
    "Cache-Control":    "max-age=86400",
}

# DEFAULT_FILE_STORAGE = "ddutils.S3.MediaS3BotoStorage"
# STATICFILES_STORAGE = "ddutils.S3.StaticS3BotoStorage"

# STATIC_URL = AWS_S3_BUCKET + "/static/"
# MEDIA_URL = AWS_S3_BUCKET + "/media/"


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################
MIDDLEWARE_CLASSES = (
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################
# CACHES = {
#     "default": {
#         "BACKEND":  config("CACHE_BACKEND", default=""),
#         "LOCATION": config("CACHE_LOCATION", default=""),
#         "TIMEOUT":  config("CACHE_TIMEOUT", default=""),
#     }
# }

# CACHE_MIDDLEWARE_ALIAS = config("CACHE_MIDDLEWARE_ALIAS", default="")
# CACHE_MIDDLEWARE_SECONDS = config("CACHE_MIDDLEWARE_SECONDS", default="")
# CACHE_MIDDLEWARE_KEY_PREFIX = config("CACHE_MIDDLEWARE_KEY_PREFIX", default="")


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################
