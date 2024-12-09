"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import inspect
import logging

from io import BytesIO

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

import papertrail

from PIL import Image
from termcolor import cprint

from ddcore.Utilities import (
    get_website_title,
    get_youtube_video_id,
    validate_url)
from ddcore.models.Attachment import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl)

from .models import Feature


logger = logging.getLogger("py.warnings")


def adjust_size(
        original_width: int, original_height: int, max_width: int, max_height: int):
    """Adjust Image Size, according to one of the providing Sides.

    Parameters
    ----------
    max_width               :int        Maximum Width.
    max_height              :int        Maximum Height.

    Returns
    -------
                            :tuple
    Raises
    ------

    """
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    new_width, new_height = None, None

    if max_width:
        new_width = max_width
        new_height = int((max_width / original_width) * original_height)
    elif max_height:
        new_width = int((max_height / original_height) * original_width)
        new_height = max_height

    return new_width, new_height


def process(request, content_type, object_id, tmp_files, tmp_links):
    """Process Instance's Attachments.

    Parameters
    ----------
    request                 :obj        Request Object.
    content_type            :obj        Content Type.
    object_id               :obj        Content Object ID.

    tmp_files               :list       List of temporary Files.
    tmp_links               :list       List of temporary Links.

    Returns
    -------

    Raises
    ------
    IOError
    SyntaxError

    """
    # -------------------------------------------------------------------------
    # --- Initials.
    # -------------------------------------------------------------------------
    subscription_plan = settings.SUBSCRIPTION_PLANS["BASIC"]

    max_width = subscription_plan["attachments"]["images"]["max_width"]
    max_height = subscription_plan["attachments"]["images"]["max_height"]

    # -------------------------------------------------------------------------
    # --- Save temporary Files.
    # -------------------------------------------------------------------------
    cprint(f"[---  INFO   ---] FILES        : {tmp_files}", "cyan")
    for tmp_file in tmp_files:
        data = {
            "original-file-name":   tmp_file.name,
            "original-file-size":   tmp_file.file.size,
        }
        file_ext = tmp_file.file.name.split(".")[-1].lower()

        cprint(f"[---  INFO   ---] TMP  FILE      : {tmp_file}\n"
               f"                  TMP  FILE EXT  : {file_ext}\n"
               f"                  TMP  FILE SIZE : {tmp_file.file.size}\n"
               f"                  FILE  IN  IMGS : {file_ext in settings.SUPPORTED_IMAGES}\n"
               f"                  FILE  IN  DOCS : {file_ext in settings.SUPPORTED_DOCUMENTS}", "cyan")

        if file_ext in settings.SUPPORTED_IMAGES:
            # -----------------------------------------------------------------
            # --- START SANITIZING IMAGE
            # -----------------------------------------------------------------
            try:
                # -------------------------------------------------------------
                # --- Verify Image.
                img = Image.open(tmp_file.file)
                img.verify()

                # -------------------------------------------------------------
                # --- Reopen Image, because `img.verify()` moves Pointer to the End of the File.
                img = Image.open(tmp_file.file)

                # cprint(f"[---  DUMP   ---] Image's original Size : {img.size}\n"
                #        f"                  Image's File Format   : {img.format}\n"
                #        f"                  Image’s Pixel Format  : {img.mode}\n"
                #        f"                  Image's Palette       : {img.palette}", "yellow")

                data.update({
                    "original-file-dimensions": img.size,
                    "original-file-format":     img.format,
                    "original-file-mode":       img.mode,
                    "original-file-palette":    img.palette,
                })

                # -------------------------------------------------------------
                # --- Convert PNG to RGB.
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                if Feature.is_enabled(request, slug="resize-images"):
                    # ---------------------------------------------------------
                    # --- Calculate new Dimensions to maintain Aspect Ratio.
                    original_width, original_height = img.size
                    new_width, new_height = None, None

                    if (
                            original_width >= original_height and
                            original_width > max_width):
                        # --- Handle horizontally-oriented Image.
                        new_width, new_height =\
                            adjust_size(original_width, original_height, max_width, None)

                        # --- Handle Panorama Style Image.
                        if new_height < max_height * 0.9:
                            new_width, new_height =\
                                adjust_size(original_width, original_height, None, max_height)
                    elif (
                            original_height >= original_width and
                            original_height > max_height):
                        # --- Handle vertically-oriented Image.
                        new_width, new_height =\
                            adjust_size(original_width, original_height, None, max_height)

                        # --- Handle Panorama Style Image.
                        if new_width < max_width * 0.9:
                            new_width, new_height =\
                                adjust_size(original_width, original_height, max_width, None)
                    else:
                        pass

                    cprint(f"[---  INFO   ---] Calculated new Dimensions\n"
                           f"                  Image's new Width  : {new_width}\n"
                           f"                  Image's new Height : {new_height}", "cyan")

                    # ---------------------------------------------------------
                    # --- Resize the image.
                    if (
                            new_width and
                            new_height):
                        img = img.resize((new_width, new_height), Image.LANCZOS)

                # -------------------------------------------------------------
                # --- Prepare the Image and save as JPEG.
                temp_img = BytesIO()
                img.save(temp_img, format="JPEG", quality=100, optimize=True)

                data.update({
                    "new-file-size":        temp_img.tell(),
                    "new-file-dimensions":  img.size,
                    "new-file-format":      img.format,
                    "new-file-mode":        img.mode,
                    "new-file-palette":     img.palette,
                })

                temp_img.seek(0)

                # -------------------------------------------------------------
                # --- Change File's Extension to `.jpg`
                original_name, _ = tmp_file.name.lower().split(".")
                new_name = f"{original_name}.jpg"

                # cprint(f"[---  INFO   ---] Resize the Image\n"
                #        f"                  Original Name : {original_name}\n"
                #        f"                  New      Name : {new_name}\n"
                #        f"                  New      Size : {img.size}\n", "cyan")

                # -------------------------------------------------------------
                # --- Save the `BytesIO` Object to the `ImageField` with the new Filename.
                attached_image = AttachedImage.objects.create(
                    name=new_name,
                    content_type=content_type,
                    object_id=object_id)
                attached_image.image.save(new_name, ContentFile(temp_img.read()), save=False)
                attached_image.save()

            except (IOError, SyntaxError) as exc:
                cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                       f"                 {type(exc).__name__}\n"
                       f"                 {str(exc)}", "white", "on_red")

                raise ValueError(f"The uploaded File is not a valid Image. -- {exc}") from exc

            except Exception as exc:
                cprint(f"### EXCEPTION @ `{inspect.stack()[0][3]}`:\n"
                       f"                 {type(exc).__name__}\n"
                       f"                 {str(exc)}", "white", "on_red")

                raise ValueError(f"The uploaded File is not a valid Image. -- {exc}") from exc

            else:
                # -------------------------------------------------------------
                # --- Save the Log.
                papertrail.log(
                    event_type="attached-image",
                    message=f"Image attached by <{request.user}> for <{attached_image.content_object}>",
                    data=data,
                    # timestamp=timezone.now(),
                    targets={
                        "user":         request.user,
                        "instance":     attached_image.content_object,
                        "attachment":   attached_image,
                    })

            finally:
                pass

        elif file_ext in settings.SUPPORTED_DOCUMENTS:
            attached_document = AttachedDocument.objects.create(
                name=tmp_file.name,
                document=File(storage.open(tmp_file.file.name, "rb")),
                content_type=content_type,
                object_id=object_id)

            # -----------------------------------------------------------------
            # --- Save the Log.
            papertrail.log(
                event_type="attached-document",
                message=f"Document attached by <{request.user}> for <{attached_document.content_object}>",
                data=data,
                # timestamp=timezone.now(),
                targets={
                    "user":         request.user,
                    "instance":     attached_document.content_object,
                    "attachment":   attached_document,
                })

        tmp_file.delete()

    # -------------------------------------------------------------------------
    # --- Save URLs and Video URLs and pull their Titles.
    # -------------------------------------------------------------------------
    cprint(f"[---  INFO   ---] LINKS        : {tmp_links}", "cyan")
    for link in tmp_links.split():
        url = validate_url(link)

        if get_youtube_video_id(link):
            AttachedVideoUrl.objects.create(
                url=link,
                content_type=content_type,
                object_id=object_id)
        elif url:
            AttachedUrl.objects.create(
                url=url,
                title=get_website_title(url) or "",
                content_type=content_type,
                object_id=object_id)
