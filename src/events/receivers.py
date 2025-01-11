"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging

from termcolor import cprint

from django.dispatch import receiver
from django.shortcuts import (
    get_object_or_404,
    render)

from privateurl.models import PrivateUrl
from privateurl.signals import (
    privateurl_ok,
    privateurl_fail)

from app.decorators import log_default
from events.models import Event


logger = logging.getLogger(__name__)


@receiver(privateurl_ok, sender=PrivateUrl)
@log_default(my_logger=logger, cls_or_self=False)
def access_private_event(sender, request, obj, action, **kwargs):
    """Docstring."""
    cprint(f"    [--- INFO ---] REQUEST  : {request}\n"
           f"                   OBJ      : {obj}\n"
           f"                   OBJ DATA : {obj.data}\n"
           f"                   ACTION   : {action}", "cyan")

    if action != "access-private-event":
        return

    if obj.user:
        obj.user.access_private_event(request=request)

    event = get_object_or_404(
        Event,
        uid=obj.data["uid"],
        slug=obj.data["slug"])

    return {
        "response": render(
            request, "events/event-details-info.html", {
                "event":                event,
                "meta":                 event.as_meta(request),
                "participation":        None,
                "is_admin":             False,
                "show_rate_form":       False,
                "show_complain_form":   False,
                # "is_newly_created":             is_newly_created,
                # "social_links":                 social_links,
            })}


@receiver(privateurl_fail, sender=PrivateUrl)
@log_default(my_logger=logger, cls_or_self=False)
def access_private_event_fail(sender, request, obj, action, **kwargs):
    """Docstring."""
    cprint(f"    [--- INFO ---] REQUEST  : {request}\n"
           f"                   OBJ      : {obj}\n"
           f"                   OBJ DATA : {obj.data}\n"
           f"                   ACTION   : {action}", "cyan")

    if action != "access-private-event":
        return

    if obj:
        # private url is expired or has exceeded ``hits_limit``
        pass
    else:
        # private url doesn't exists or token in url is not correct
        pass


# m2m_changed.connect(toppings_changed, sender=Pizza.toppings.through)
