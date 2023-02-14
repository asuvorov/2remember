from django.conf import settings
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError


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
