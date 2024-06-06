"""
(C) 2013-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

import os

from django.core.wsgi import get_wsgi_application

# from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

application = get_wsgi_application()
# application = WhiteNoise(application, root="/opt/apps/saneside/src/staticserve")
