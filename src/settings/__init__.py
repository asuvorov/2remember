"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import django

from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy

django.utils.encoding.smart_text = smart_str
django.utils.encoding.smart_unicode = smart_str
django.utils.translation.ugettext_lazy = gettext_lazy
