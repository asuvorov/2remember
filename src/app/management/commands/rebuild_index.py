"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

# from django.core.management.base import BaseCommand

# from haystack.management.commands import rebuild_index


# class Command(BaseCommand):
#     """Rebuild/update Search Indexes.

#     https://stackoverflow.com/questions/4358771/updating-a-haystack-search-index-with-django-celery
#     """

#     help = "Rebuild/update Search Indexes."

#     def handle(self, *args, **kwargs):
#         rebuild_index.Command().handle(
#             age=4,
#             batchsize=1000,
#             workers=0,
#             max_retries=5,
#             interactive=False,
#             remove=True,
#             verbosity=2,
#             using=["default", ])

#         self.stdout.write("!!! Successfully rebuilt Indexes !!!\n")
