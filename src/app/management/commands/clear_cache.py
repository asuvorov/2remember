"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

from django.conf import settings
from django.core.cache import cache
from django.core.management.base import (
    BaseCommand,
    CommandError)


class Command(BaseCommand):
    """A simple Management Command, which clears the Site-wide Cache."""

    help = "Fully clear your Site-wide Cache."

    def handle(self, *args, **kwargs):
        try:
            assert settings.CACHES

            cache.clear()

            self.stdout.write("!!! Your Cache has been cleared!\n")

        except AttributeError as exc:
            raise CommandError("### You have no Cache configured!\n") from exc
