"""Application."""

import django

from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy


django.utils.encoding.smart_unicode = smart_str
django.utils.translation.ugettext_lazy = gettext_lazy
