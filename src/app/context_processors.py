"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings

from ddcore.models import (
    SocialApp, social_app_choices,
    SocialAppIcons, social_app_icons,
    SocialAppButtons, social_app_buttons)


def pb_settings(request):
    """Docstring."""
    return {
        "product_version_num":  settings.PRODUCT_VERSION_NUM,
        "ENVIRONMENT":          settings.ENVIRONMENT,
    }


def pb_social_link_choices(request):
    """Docstring."""
    return {
        "SocialApp":            SocialApp,
        "social_app_choices":   social_app_choices,
        "SocialAppIcons":       SocialAppIcons,
        "social_app_icons":     social_app_icons,
        "SocialAppButtons":     SocialAppButtons,
        "social_app_buttons":   social_app_buttons,
    }


def pb_social_links(request):
    """Docstring."""
    return {
        "PB_SOCIAL_LINKS":      settings.PB_SOCIAL_LINKS,
    }


def pb_supported_media(request):
    """Docstring."""
    return {
        "documents":            settings.SUPPORTED_DOCUMENTS,
        "documents_str":        settings.SUPPORTED_DOCUMENTS_STR,
        "documents_str_ext":    settings.SUPPORTED_DOCUMENTS_STR_EXT,
        "documents_str_reg":    settings.SUPPORTED_DOCUMENTS_STR_REG,
        "images":               settings.SUPPORTED_IMAGES,
        "images_str":           settings.SUPPORTED_IMAGES_STR,
        "images_str_ext":       settings.SUPPORTED_IMAGES_STR_EXT,
        "images_str_reg":       settings.SUPPORTED_IMAGES_STR_REG,
    }
