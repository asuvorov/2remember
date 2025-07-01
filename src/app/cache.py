"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _

from annoying.functions import get_object_or_None

from events.models import Event
from organizations.models import Organization


UPLOAD_NUMBERS_CACHE_KEY = "upload_numbers_{}_{}"
UPLOAD_NUMBERS_DEFAULT = {
    "images": {
        "max":      0,
        "saved":    0,
        "temps":    0,
        "total":    0,
    },
    "documents": {
        "max":      0,
        "saved":    0,
        "temps":    0,
        "total":    0,
    },
    "video": {
        "max":      0,
        "saved":    0,
        "temps":    0,
        "total":    0,
    },
}


def get_upload_numbers(instance_type, instance_uid: str):
    """Docstring."""
    cache_key = UPLOAD_NUMBERS_CACHE_KEY.format(instance_type, instance_uid)
    subscription_plan = settings.SUBSCRIPTION_PLANS[settings.SUBSCRIPTION_PLAN_DEFAULT]

    # -------------------------------------------------------------------------
    # --- Pull out cached Data.
    # -------------------------------------------------------------------------
    upload_numbers = cache.get(cache_key)
    if not upload_numbers:
        # ---------------------------------------------------------------------
        # --- Pull the Instance.
        if instance_type == "event":
            instance = get_object_or_None(Event, uid=instance_uid)
        elif instance_type == "organization":
            instance = get_object_or_None(Organization, uid=instance_uid)

        if not instance:
            return None, _("Instance not found.")

        # ---------------------------------------------------------------------
        # --- Pull the Instance's saved and temporary Images.
        saved_images = instance.image_count

        # ---------------------------------------------------------------------
        # --- Pull the Instance's saved and temporary Documents.
        saved_documents = instance.document_count

        # ---------------------------------------------------------------------
        # --- Pull the Instance's saved and temporary Video.

        # ---------------------------------------------------------------------
        # --- Prepare Payload.
        upload_numbers = {
            "images": {
                "max":      subscription_plan["attachments"]["images"][f"max_per_{instance_type}"],
                "saved":    saved_images,
                "temps":    0,
                "total":    saved_images,
            },
            "documents": {
                "max":      subscription_plan["attachments"]["documents"][f"max_per_{instance_type}"],
                "saved":    saved_documents,
                "temps":    0,
                "total":    saved_documents,
            },
            "video": {
                "max":      subscription_plan["attachments"]["video"][f"max_per_{instance_type}"],
                "saved":    0,
                "temps":    0,
                "total":    0,
            },
        }

        cache.set(cache_key, upload_numbers, 3600)

    return upload_numbers, ""


def set_upload_numbers(instance_type, instance_uid: str, upload_numbers: dict):
    """Docstring."""
    cache_key = UPLOAD_NUMBERS_CACHE_KEY.format(instance_type, instance_uid)

    cache.set(cache_key, upload_numbers, 3600)


def del_upload_numbers(instance_type, instance_uid: str):
    """Docstring."""
    cache_key = UPLOAD_NUMBERS_CACHE_KEY.format(instance_type, instance_uid)

    cache.delete(cache_key)
