"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from .forms import LoginForm


def signin_form(request):
    """Docstring."""
    signin_form = LoginForm()

    return {
        "signin_form":  signin_form,
    }
