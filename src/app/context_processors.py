"""Define Context Processors."""

from django.conf import settings

from ddcore.models.choices import (
    SocialApp, social_app_choices,
    SocialAppIcons, social_app_icons,
    SocialAppButtons, social_app_buttons)


def pb_settings(request):
    """Docstring."""
    return {
        "product_version_full":     settings.PRODUCT_VERSION_FULL,
        "product_version_num":      settings.PRODUCT_VERSION_NUM,
        "ENVIRONMENT":              settings.ENVIRONMENT,
    }


def pb_social_links(request):
    """Docstring."""
    return {
        "PB_SOCIAL_LINKS":          settings.PB_SOCIAL_LINKS,
    }


def pb_social_link_choices(request):
    """Docstring."""
    return {
        "SocialApp":               SocialApp,
        "social_app_choices":       social_app_choices,
        "SocialAppIcons":         SocialAppIcons,
        "social_app_icons":         social_app_icons,
        "SocialAppButtons":       SocialAppButtons,
        "social_app_buttons":       social_app_buttons,
    }