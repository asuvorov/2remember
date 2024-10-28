"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import json
import logging
import mimetypes

from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    JsonResponse)
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from annoying.functions import get_object_or_None
from termcolor import cprint

from ddcore.models.Attachment import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl,
    TemporaryFile)

from . import logconst
from .decorators import log_default
from .logformat import Format
from .management.commands import clear_cache


logger = logging.getLogger(__name__)


# =============================================================================
# ===
# === HANDLERS
# ===
# =============================================================================
@log_default(my_logger=logger, cls_or_self=False)
def handler400(request, exception=None):
    """400 Handler."""
    cprint(f"###" * 27, "white", "on_red")
    cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
           f"{type(exception).__name__} : {str(exception)}",
           "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    return render(request, "error-pages/400.html", status=404)


@log_default(my_logger=logger, cls_or_self=False)
def handler403(request, exception=None):
    """403 Handler."""
    cprint(f"###" * 27, "white", "on_red")
    cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
           f"{type(exception).__name__} : {str(exception)}",
           "white", "on_red")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.exception("", extra=Format.exception(
        exc=exception,
        request_id=request.request_id,
        log_extra={}))

    return render(request, "error-pages/403.html", status=404)


@log_default(my_logger=logger, cls_or_self=False)
def handler404(request, exception=None):
    """404 Handler."""
    cprint(f"###" * 27, "white", "on_red")
    cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
           f"{type(exception).__name__} : {str(exception)}",
           "white", "on_red")

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
    """500 Handler."""
    cprint(f"###" * 27, "white", "on_red")
    cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
           f"{type(exception).__name__} : {str(exception)}",
           "white", "on_red")

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
        cprint(f"###" * 27, "white", "on_red")
        cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
               f"{type(exc).__name__} : {str(exc)}",
               "white", "on_red")

        # ---------------------------------------------------------------------
        # --- Logging.
        # ---------------------------------------------------------------------
        logger.exception("", extra=Format.exception(
            exc=exception,
            request_id=request.request_id,
            log_extra={}))

    return render(request, "error-pages/500.html", status=500)


# =============================================================================
# ===
# === ATTACHMENTS
# ===
# =============================================================================
@login_required
@require_http_methods(["POST", ])
@log_default(my_logger=logger, cls_or_self=False)
def tmp_upload(request):
    """Upload temporary File."""
    if not request.FILES:
        return HttpResponseBadRequest(
            _("No Files attached."))

    tmp_file = TemporaryFile.objects.create(
        file=request.FILES["file"],
        name=request.FILES["file"].name)

    result = {
        "file_name":    tmp_file.file.name,
        "file_type":    mimetypes.guess_type(tmp_file.file.name)[0] or "image/png",
        "file_size":    tmp_file.file.size,
        "tmp_file_id":  tmp_file.id,
    }

    cprint(f"[---  INFO   ---] TMP  FILE      : {result}", "cyan")

    # -------------------------------------------------------------------------
    # --- Logging.
    # -------------------------------------------------------------------------
    logger.info("REQUEST", extra=Format.api_detailed_info(
        log_type=logconst.LOG_VAL_TYPE_API_REQUEST,
        request_id=request.request_id,
        log_extra=result.copy()))

    return JsonResponse({
        "files":    [result],
    })


@login_required
@require_http_methods(["POST", ])
@log_default(my_logger=logger, cls_or_self=False)
def remove_upload(request):
    """Remove uploaded File."""
    found = False

    upload_type = request.POST.get("type")
    upload_id = request.POST.get("id")

    if upload_type and upload_id:
        if upload_type == "document":
            instance = get_object_or_None(AttachedDocument, id=upload_id)
        elif upload_type == "image":
            instance = get_object_or_None(AttachedImage, id=upload_id)
        elif upload_type == "temp":
            instance = get_object_or_None(TemporaryFile, id=upload_id)

        if instance:
            try:
                instance.file.delete()
            except Exception as exc:
                cprint(f"###" * 27, "white", "on_red")
                cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`: "
                       f"{type(exc).__name__} : {str(exc)}",
                       "white", "on_red")

                # -------------------------------------------------------------
                # --- Logging.
                # -------------------------------------------------------------
                logger.exception("", extra=Format.exception(
                    exc=exc,
                    request_id=request.request_id,
                    log_extra={}))

            instance.delete()
            found = True

    return JsonResponse({
        "deleted":  found,
    })


@login_required
@require_http_methods(["POST", ])
@log_default(my_logger=logger, cls_or_self=False)
def remove_link(request):
    """Remove Link."""
    found = False

    upload_type = request.POST.get("type")
    upload_id = request.POST.get("id")

    if upload_type and upload_id:
        if upload_type == "regular":
            instance = get_object_or_None(AttachedUrl, id=upload_id)
        elif upload_type == "video":
            instance = get_object_or_None(AttachedVideoUrl, id=upload_id)

        if instance:
            instance.delete()
            found = True

    return JsonResponse({
        "deleted":  found,
    })
