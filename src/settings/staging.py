"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from decouple import config

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *


# -----------------------------------------------------------------------------
# --- Override Settings here.
# -----------------------------------------------------------------------------
DEBUG = True


###############################################################################
### AWS SETTINGS                                                            ###
###############################################################################
# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
# https://www.makeuseof.com/django-aws-s3-bucket-host-static-media-files/
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_BUCKET_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_PRELOAD_METADATA = config("AWS_PRELOAD_METADATA", default=True, cast=bool)
AWS_QUERYSTRING_AUTH = config("AWS_QUERYSTRING_AUTH", default=False, cast=bool)
AWS_DEFAULT_ACL = "public-read"
AWS_HEADERS = {
    "Cache-Control":    "max-age=86400",
}
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl":     "max-age=86400",
}

DEFAULT_FILE_STORAGE = "app.S3.PublicMediaS3BotoStorage"
STATICFILES_STORAGE = "app.S3.CachedS3BotoStorage"
STATIC_URL = f"https://{AWS_S3_BUCKET_DOMAIN}/static/"
MEDIA_URL = f"https://{AWS_S3_BUCKET_DOMAIN}/media/"


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
CACHE_MIDDLEWARE_ALIAS = config("CACHE_MIDDLEWARE_ALIAS", default="locmem")
CACHE_MIDDLEWARE_SECONDS = config("CACHE_MIDDLEWARE_SECONDS", default=60)
CACHE_MIDDLEWARE_KEY_PREFIX = config("CACHE_MIDDLEWARE_KEY_PREFIX", default="staging")


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################


###############################################################################
### DJANGO COMPRESSOR                                                       ###
###############################################################################
# https://django-compressor.readthedocs.io/en/stable/remote-storages.html
COMPRESS_STORAGE = STATICFILES_STORAGE
COMPRESS_OFFLINE_MANIFEST_STORAGE = STATICFILES_STORAGE
COMPRESS_URL = STATIC_URL
