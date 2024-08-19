"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging

from django.http import HttpResponse
from django.shortcuts import render

from termcolor import cprint

from .decorators import log_default
from .logformat import Format
from .management.commands import clear_cache


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === HANDLERS
# ===
# =============================================================================
def permission_denied_handler(request):
    """Permission denied Handler."""
    return HttpResponse("You have no Permissions!")


def resource_access_handler(request, resource):
    """Callback for resource access.

    Determines who can see the documentation for which API.
    """
    # -------------------------------------------------------------------------
    # --- Superusers and Staff can see whatever they want
    if (
            request.user.is_superuser or
            request.user.is_staff):
        return True

    return False


@log_default(my_logger=logger, cls_or_self=False)
def handler400(request, exception=None):
    """400 Handler (Bad Request)."""
    if exception:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exception).__name__}\n"
               f"                 {str(exception)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    return render(request, "error-pages/400.html", status=400)


@log_default(my_logger=logger, cls_or_self=False)
def handler403(request, exception=None):
    """403 Handler (Forbidden / Permission Denied)."""
    if exception:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exception).__name__}\n"
               f"                 {str(exception)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    return render(request, "error-pages/403.html", status=403)


@log_default(my_logger=logger, cls_or_self=False)
def handler404(request, exception=None):
    """404 Handler (Not Found)."""
    if exception:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exception).__name__}\n"
               f"                 {str(exception)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    return render(request, "error-pages/404.html", status=404)


@log_default(my_logger=logger, cls_or_self=False)
def handler500(request, exception=None):
    """500 Handler (Internal Server Error)."""
    if exception:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exception).__name__}\n"
               f"                 {str(exception)}", "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    try:
        clear_cache.Command().handle()

        # ---------------------------------------------------------------------
        # --- Save the Log

    except Exception as exc:
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
               f"                 {type(exc).__name__}\n"
               f"                 {str(exc)}", "white", "on_red")

        # ---------------------------------------------------------------------
        # --- Logging.
        # ---------------------------------------------------------------------
        logger.exception("", extra=Format.exception(
            exc=exception,
            request_id=request.request_id,
            log_extra={}))

    return render(request, "error-pages/500.html", status=500)
