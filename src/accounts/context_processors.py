"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

from .forms import LoginForm


def signin_form(request):
    """Docstring."""
    signin_form = LoginForm()

    return {
        "signin_form":  signin_form,
    }
