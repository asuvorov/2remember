"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

# import datetime

# from haystack import indexes

# from .choices import PostStatus
# from .models import Post


# # -----------------------------------------------------------------------------
# # --- POST SEARCH INDEX
# # -----------------------------------------------------------------------------
# class PostIndex(indexes.SearchIndex, indexes.Indexable):
#     """Post Index."""

#     # -------------------------------------------------------------------------
#     text = indexes.CharField(
#         document=True,
#         use_template=True)
#     rendered = indexes.CharField(
#         use_template=True,
#         indexed=False)

#     # -------------------------------------------------------------------------
#     author = indexes.CharField(model_attr="author")
#     title = indexes.CharField(model_attr="title")
#     content = indexes.CharField(
#         model_attr="content",
#         default="")

#     created = indexes.DateTimeField(model_attr="created")

#     def get_model(self):
#         """Docstring."""
#         return Post

#     def index_queryset(self, using=None):
#         """Used when the entire Index for Model is updated."""
#         return self.get_model().objects.filter(
#             status=PostStatus.VISIBLE,
#             created__lte=datetime.date.today())
