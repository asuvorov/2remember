"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
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
