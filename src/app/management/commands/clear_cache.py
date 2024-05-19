"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import (
    BaseCommand,
    CommandError)


class Command(BaseCommand):
    """A simple management command which clears theSite-wide Cache."""

    help = "Fully clear your Site-wide Cache."

    def handle(self, *args, **kwargs):
        try:
            assert settings.CACHES

            cache.clear()

            self.stdout.write("!!! Your Cache has been cleared!\n")

        except AttributeError:
            raise CommandError("## You have no Cache configured!\n")
