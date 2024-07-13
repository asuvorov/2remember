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
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
# AWS_S3_BUCKET_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_PRELOAD_METADATA = config("AWS_PRELOAD_METADATA", default=True, cast=bool)
# AWS_QUERYSTRING_AUTH = config("AWS_QUERYSTRING_AUTH", default=False, cast=bool)
# AWS_DEFAULT_ACL = "public-read"
# AWS_HEADERS = {
#     "Cache-Control":    "max-age=86400",
# }
# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl":     "max-age=86400",
# }

# DEFAULT_FILE_STORAGE = "app.S3.PublicMediaS3BotoStorage"
# STATICFILES_STORAGE = "app.S3.CachedS3BotoStorage"
# STATIC_URL = f"https://{AWS_S3_BUCKET_DOMAIN}/static/"
# MEDIA_URL = f"https://{AWS_S3_BUCKET_DOMAIN}/media/"


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################


###############################################################################
### DJANGO COMPRESSOR                                                       ###
###############################################################################
# https://django-compressor.readthedocs.io/en/stable/remote-storages.html
# COMPRESS_STORAGE = STATICFILES_STORAGE
# COMPRESS_OFFLINE_MANIFEST_STORAGE = STATICFILES_STORAGE
# COMPRESS_URL = STATIC_URL
