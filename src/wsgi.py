"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import os

from django.core.wsgi import get_wsgi_application

# from whitenoise import WhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

application = get_wsgi_application()
# application = WhiteNoise(application, root="/opt/apps/saneside/src/staticserve")
