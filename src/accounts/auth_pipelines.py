"""Define Auth Pipelines."""

import requests

from django.core.files.base import ContentFile

from requests import HTTPError

from .models import (
    UserProfile,
    UserLogin)


def save_profile(
        strategy, backend, uid, response, details, user, social, request, is_new=False,
        *args, **kwargs):
    """Docstring."""
    avatar_url = ""

    try:
        profile = user.profile
    except Exception as exc:
        print(f"### EXCEPTION : {type(exc).__name__} : {str(exc)}")

        profile = UserProfile.objects.create(user=user)

    # -------------------------------------------------------------------------
    # --- FACEBOOK.
    # -------------------------------------------------------------------------
    if is_new and backend.name == "facebook":
        # profile.gender = response.get("gender").capitalize()
        profile.fb_profile = response.get("link")

        avatar_url =f"http://graph.facebook.com/{response.get('id')}/picture?type=large"

    # -------------------------------------------------------------------------
    # --- LINKEDIN.
    # -------------------------------------------------------------------------
    if backend.name == "linkedin":
        pass

    # -------------------------------------------------------------------------
    # --- GOOGLE-PLUS.
    # -------------------------------------------------------------------------
    if backend.name == "google-oauth2":
        if response.get("image") and response["image"].get("url"):
            avatar_url = response["image"].get("url")

    # -------------------------------------------------------------------------
    # --- Import social Profile Avatar.
    # -------------------------------------------------------------------------
    if (
            avatar_url and (
                is_new or not profile.avatar)):
        try:
            response = requests.get(avatar_url)
            response.raise_for_status()
        except HTTPError:
            pass
        else:
            profile.avatar.save(f"{user.username}_social.jpg", ContentFile(response.content))
    else:
        # ---------------------------------------------------------------------
        # --- If existing Avatar, stick with it.
        pass

    profile.save()

    # -------------------------------------------------------------------------
    # --- Track IP.
    # -------------------------------------------------------------------------
    UserLogin.objects.insert(
        request=strategy.request,
        user=user,
        provider=backend.name)

    # -------------------------------------------------------------------------
    # --- Save the Log.