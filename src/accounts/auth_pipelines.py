"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging
import requests

from django.core.files.base import ContentFile

from requests import HTTPError
from termcolor import cprint

from ddcore.models import UserLogin

# pylint: disable=import-error
from app.decorators import log_default

from .models import UserProfile


logger = logging.getLogger(__name__)


@log_default(my_logger=logger, cls_or_self=False)
def save_profile(
        strategy, backend, uid, response, details, user, social, request, is_new=False,
        *args, **kwargs):
    """Docstring."""
    avatar_url = ""

    cprint(f"[---  INFO   ---] STRATEGY             : {strategy}", "cyan")
    cprint(f"                  BACKEND              : {backend}", "cyan")
    cprint(f"                  UID                  : {uid}", "cyan")
    cprint(f"                  RESPONSE             : {response}", "cyan")
    cprint(f"                  DETAILS              : {details}", "cyan")
    cprint(f"                  USER                 : {user}", "cyan")
    cprint(f"                  SOCIAL               : {social}", "cyan")
    cprint(f"                  REQUEST              : {request}", "cyan")
    cprint(f"                  IS NEW               : {is_new}", "cyan")

    try:
        profile = user.profile
    except Exception as exc:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exc).__name__}\n"
               f"                 {str(exc)}", "white", "on_red")

        profile = UserProfile.objects.create(user=user)

    # -------------------------------------------------------------------------
    # --- FACEBOOK
    # -------------------------------------------------------------------------
    if is_new and backend.name == "facebook":
        # profile.gender = response.get("gender").capitalize()
        profile.fb_profile = response.get("link")

        avatar_url = f"http://graph.facebook.com/{response.get('id')}/picture?type=large"

    # -------------------------------------------------------------------------
    # --- TWITTER
    # -------------------------------------------------------------------------
    if backend.name == "twitter":
        pass

    # -------------------------------------------------------------------------
    # --- LINKEDIN
    # -------------------------------------------------------------------------
    if backend.name == "linkedin":
        pass

    # -------------------------------------------------------------------------
    # --- Import social Profile Avatar.
    # -------------------------------------------------------------------------
    if (
            avatar_url and (
                is_new or
                not profile.avatar)):
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
