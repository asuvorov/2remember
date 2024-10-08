"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import os

from os import path
from setuptools import (
    find_packages,
    setup)


here = path.abspath(path.dirname(__file__))


# -----------------------------------------------------------------------------
# --- Get the long Description from the `README` File.
# -----------------------------------------------------------------------------
with open(path.join(here, "README.md"), "r") as f:
    """Docstring."""
    long_description = f.read()


def package_files(directory, home_dir):
    """Docstring."""
    paths = []
    # -------------------------------------------------------------------------
    # --- Iterate over the Directory, passed here.
    for (p, directories, filenames) in os.walk(directory):
        files = []

        for filename in filenames:
            files.append(os.path.join(p, filename))

        paths.append((os.path.join(home_dir, "src", *p.split(os.sep)[1:]), files))

    return paths


setup(
    name="2remember",
    version="0.4.0",
    description="",
    long_description=long_description,
    url="https://github.com/asuvorov/2remember",
    author="",
    author_email="",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 5 - Production/Stable",
        "Environment :: UNIX System V",
        "Framework :: Sphinx",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9.6",
        "Topic :: Database",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Games/Entertainment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: Content Management System",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    install_requires=[
        # "APScheduler==3.9.1",
        "djangorestframework==3.15.1",
        # "djangorestframework-jsonp==1.0.2",
        "django-admin-rangefilter==0.12.4",
        "django-admin-sortable2==2.1.10",
        # "django-bootstrap3-datetimepicker==2.2.3",
        "django-bower==5.2.0",
        "django-compressor==4.4",
        "django-cors-headers-4.4.0",
        # "django-debug-toolbar==3.8.1",
        # "django-easy-pdf==0.1.1",
        # "django-easy-timezones==0.8.0",
        "django-filter==24.2",
        "django-formset-js==0.5.0",
        "django-geoip2-extras==4.1",
        "django-grappelli==4.0.1",
        # "django-haystack==3.2.1",
        "django-imagekit==5.0.0",
        "django-meta==2.4.2",
        "django-passwords==0.3.12",
        "django-profanity-filter==0.2.1",
        "django-rosetta==0.10.0",
        # "django-secure==1.0.2",
        # "django-simple-captcha==0.5.17",
        # "django-sslserver==0.22",
        "django-static-fontawesome==6.5.2.0",
        "django-static-ionicons==2.0.1.5",
        "django-taggit==5.0.1",
        "django-taggit-templatetags2==1.6.1",
        "django-timezone-field==6.1.0",
        "django-twitter-tag==1.2.1",
        "django-url-tools-py3==0.2.1",
        # "elasticsearch==8.6.1",
        "gunicorn==23.0.0",
        "lxml==5.2.1",
        "mysqlclient==2.2.4",
        "pymemcache==4.0.0",
        "pytz==2024.1",
        # "sendgrid-django==4.2.0",
        "sentry-sdk[django]==2.7.1",
        "social-auth-app-django==5.4.2",
        "whitenoise==6.6.0",
    ],
    license="",
)
