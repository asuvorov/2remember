"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

# import datetime

# from django.db.models import Q

# from haystack import indexes

# from .choices import (
#     EventStatus,
# from .models import Event


# # -----------------------------------------------------------------------------
# # --- EVENT SEARCH INDEX
# # -----------------------------------------------------------------------------
# class EventIndex(indexes.SearchIndex, indexes.Indexable):
#     """Event Index."""

#     # -------------------------------------------------------------------------
#     text = indexes.CharField(
#         document=True,
#         use_template=True)
#     rendered = indexes.CharField(
#         use_template=True,
#         indexed=False)

#     # -------------------------------------------------------------------------
#     author = indexes.CharField(model_attr="author")
#     name = indexes.CharField(model_attr="name")
#     description = indexes.CharField(
#         model_attr="description",
#         default="")

#     created = indexes.DateTimeField(model_attr="created")

#     def get_model(self):
#         """Docstring."""
#         return Event

#     def index_queryset(self, using=None):
#         """Used when the entire Index for Model is updated."""
#         return self.get_model().objects.filter(
#             Q(organization=None) |
#             Q(organization__is_hidden=False),
#             Q(recurrence=Recurrence.DATELESS) |
#             status=EventStatus.UPCOMING)
