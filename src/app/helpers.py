"""Define Helpers."""

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
