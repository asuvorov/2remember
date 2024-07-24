"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import logging
import mimetypes

from io import BytesIO

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

from PIL import Image
from ddcore.Utilities import (
    get_website_title,
    get_youtube_video_id,
    validate_url)
from termcolor import cprint

from ddcore.models.Attachment import (
    AttachedDocument,
    AttachedImage,
    AttachedUrl,
    AttachedVideoUrl)


logger = logging.getLogger("py.warnings")


def adjust_size(
        original_width: int, original_height: int, max_width: int, max_height: int ):
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

    for tmp_file in tmp_files:
        mime_type = mimetypes.guess_type(tmp_file.file.name)[0]

        cprint("[---  INFO   ---] TMP  FILE      : %s" % tmp_file, "cyan")
        cprint("[---  INFO   ---] MIME TYPE      : %s" % mime_type, "cyan")

        if mime_type in settings.UPLOADER_SETTINGS["images"]["CONTENT_TYPES"]:
            # -----------------------------------------------------------------
            # --- START RESIZING IMAGE
            # -----------------------------------------------------------------
            try:
                # -------------------------------------------------------------
                # --- Verify Image.
                img = Image.open(tmp_file.file.name)
                img.verify()

                # -------------------------------------------------------------
                # --- Reopen Image, because `img.verify()` moves Pointer to the End of the File.
                img = Image.open(tmp_file.file.name)

                cprint(f"Image's original Size : {img.size}", "yellow")
                cprint(f"Image's File Format   : {img.format}", "yellow")
                cprint(f"Image’s Pixel Format  : {img.mode}", "yellow")
                cprint(f"Image's Palette       : {img.palette}", "yellow")

                # -------------------------------------------------------------
                # --- Convert PNG to RGB.
                if img.mode in ("RGBA", "LA", "P"):
                    img = img.convert("RGB")

                # -------------------------------------------------------------
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

                cprint(f"Image's new Width  : {new_width}", "yellow")
                cprint(f"Image's new Height : {new_height}", "yellow")

                # -------------------------------------------------------------
                # --- Resize the image.
                if new_width and new_height:
                    img = img.resize((new_width, new_height), Image.LANCZOS)

                # -------------------------------------------------------------
                # --- Prepare the Image and save as JPEG.
                temp_img = BytesIO()
                img.save(temp_img, format="JPEG", quality=90, optimize=True)
                temp_img.seek(0)

                # -------------------------------------------------------------
                # --- Change File's Extension to `.jpg`
                original_name, _ = tmp_file.name.lower().split(".")
                new_name = f"{original_name}.jpg"

                # -------------------------------------------------------------
                # --- Save the `BytesIO` Object to the `ImageField` with the new Filename.
                AttachedImage.objects.create(
                    name=new_name,
                    image=ContentFile(temp_img.read()),
                    content_type=content_type,
                    object_id=object_id)

            except (IOError, SyntaxError) as exc:
                raise ValueError(f"The uploaded file is not a valid image. -- {exc}") from exc

            except Exception as exc:
                raise ValueError(f"The uploaded file is not a valid image. -- {exc}") from exc

            # -----------------------------------------------------------------
            # ---  END  RESIZING IMAGE
            # -----------------------------------------------------------------

            # AttachedImage.objects.create(
            #     name=tmp_file.name,
            #     image=File(storage.open(tmp_file.file.name, "rb")),
            #     content_type=content_type,
            #     object_id=object_id)
        elif mime_type in settings.UPLOADER_SETTINGS["documents"]["CONTENT_TYPES"]:
            AttachedDocument.objects.create(
                name=tmp_file.name,
                document=File(storage.open(tmp_file.file.name, "rb")),
                content_type=content_type,
                object_id=object_id)

        tmp_file.delete()

    # -----------------------------------------------------------------
    # --- Save URLs and Video URLs and pull their Titles.
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
