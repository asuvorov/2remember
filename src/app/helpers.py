"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from ddcore.decorators import exception


@exception
def form_field_error_list(form):
    """Docstring."""
    form_errors = []

    for field in form:
        if field.errors:
            for error in field.errors:
                form_errors.append(f"{field.label} : {field.value()} : {error}")
        else:
            form_errors.append(f"{field.label} : {field.value()}")

    return form_errors
