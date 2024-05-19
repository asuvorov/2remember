"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

# from haystack import indexes

# from .models import FAQ


# # -----------------------------------------------------------------------------
# # --- FAQ SEARCH INDEX
# # -----------------------------------------------------------------------------
# class FAQIndex(indexes.SearchIndex, indexes.Indexable):
#     """FAQ Index."""

#     # -------------------------------------------------------------------------
#     text = indexes.CharField(
#         document=True,
#         use_template=True)
#     rendered = indexes.CharField(
#         use_template=True,
#         indexed=False)

#     # -------------------------------------------------------------------------
#     author = indexes.CharField(model_attr="author")
#     question = indexes.CharField(model_attr="question")
#     answer = indexes.CharField(
#         model_attr="answer",
#         default="")

#     created = indexes.DateTimeField(model_attr="created")

#     def get_model(self):
#         """Docstring."""
#         return FAQ

#     def index_queryset(self, using=None):
#         """Used when the entire Index for Model is updated."""
#         return self.get_model().objects.all()
