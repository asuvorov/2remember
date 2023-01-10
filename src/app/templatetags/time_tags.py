"""Define Template Tags."""

import datetime

from django import template
from django.conf import settings

import pytz


register = template.Library()


def pretty_timestamp(timestamp):
    """Docstring."""
    local_tz = pytz.timezone(settings.TIME_ZONE)

    try:
        t_s = float(timestamp)
    except ValueError:
        return None

    # Specify Format here
    # return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(t_s))
    return local_tz.localize(datetime.datetime.fromtimestamp(t_s))

register.filter(pretty_timestamp)
