"""Application."""

import django

from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy


django.utils.encoding.smart_unicode = smart_str
django.utils.translation.ugettext_lazy = gettext_lazy


# -----------------------------------------------------------------------------
# --- PRODUCT VERSIONS
# -----------------------------------------------------------------------------
PRODUCT_NAME = "Cuddly Disco Server"
RELEASE_TYPE = {
    "ALPHA":    "alpha",
    "BETA":     "beta",
    "RC":       "rc",
}

# --- Versioning Strategy
#     <major>.<minor>.<patch>[-<type><attempt>]
#     <major>.<minor>.<patch>.<build>[-<type><attempt>]

VERSION_API = 1
VERSION_NAME = "Cuddly Disco"
VERSION_YEAR = 2023
# --- Major version is a number indicating a significant change in the
#     application. A major version might possibly be a complete rewrite of the
#     previous major version and/or break backwards compatibility with older
#     versions.
VERSION_MAJOR = 0
# --- Minor version is a number that indicates a small set of changes from the
#     previous minor version. A minor version usually consists of an even set
#     of bug fixes and new features and should always be backwards compatible.
VERSION_MINOR = 0
# --- Patch is a number that indicates some bugs were fixed that could not wait
#     until the next minor release. A patch version should only include bug
#     fixes and never include new features. It should also always be backwards
#     compatible. Security fixes are an example of a typical patch.
VERSION_PATCH = 0
# --- Build Number is incremented when new build is created.
VERSION_BUILD = 0
# --- This is last part is optional and only used to identify that this version
#     is not necessarily stable. The type is a keyword and can be anything but
#     usually sticks to "alpha", "beta", and "RC".
#     The attempt is just a number to indicate which attempt at this type is
#     this. So for example, "beta-01", "RC-02", "RC-05", etc. For a stable
#     version, leave off this part, however, other projects like to use the
#     keyword of RELEASE to indicate the stable version.
VERSION_RELEASE = RELEASE_TYPE["ALPHA"]
VERSION_ATTEMPT = 1

PRODUCT_VERSION_FULL = (
    "{pname}, v.{major}.{minor}.{patch}-{rtype}{atmpt}: {vname}".format(
        pname=PRODUCT_NAME,
        major=VERSION_MAJOR,
        minor=VERSION_MINOR,
        patch=VERSION_PATCH,
        rtype=VERSION_RELEASE,
        atmpt=VERSION_ATTEMPT,
        vname=VERSION_NAME,
    )
)
PRODUCT_VERSION_NUM = (
    "v.{major}.{minor}.{patch}-{rtype}{atmpt}".format(
        major=VERSION_MAJOR,
        minor=VERSION_MINOR,
        patch=VERSION_PATCH,
        rtype=VERSION_RELEASE,
        atmpt=VERSION_ATTEMPT,
    )
)
