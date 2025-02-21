"""
(C) 2013-2025 Copycat Software, LLC. All Rights Reserved.
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from .base import *


# -----------------------------------------------------------------------------
# --- Override Settings here.
# -----------------------------------------------------------------------------
DEBUG = True

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.sqlite3",
        "NAME":     "test-sqlite.db",
        "USER":     "",
        "PASSWORD": "",
        "HOST":     "",
        "PORT":     "",
        "OPTIONS": {
            # "autocommit": True,
        }
    }
}

SUBSCRIPTION_PLANS = {
    "DAILY": {
        "fare": 0,  # Cents.
        "attachments": {
            "documents": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "images": {
                "max_width":            900,
                "max_height":           600,
                "max_file_size":        102400,
                "max_per_event":        5,
                "max_per_organization": 5,
                "quality":              80,
            },
            "video": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "video_urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
        },
        "accounts": {},
        "events": {
            "max_per_day":          1,
            "max_per_week":         None,
            "max_per_month":        None,
            "max_per_year":         None,
            "upon_request_only":    False,
        },
        "organizations": {
            "max_per_day":          1,
            "max_per_week":         None,
            "max_per_month":        None,
            "max_per_year":         None,
            "upon_request_only":    True,
        },
        "places": {},
    },
    "WEEKLY": {
        "fare": 0,  # Cents.
        "attachments": {
            "documents": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "images": {
                "max_width":            900,
                "max_height":           600,
                "max_file_size":        102400,
                "max_per_event":        5,
                "max_per_organization": 5,
                "quality":              80,
            },
            "video": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "video_urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
        },
        "accounts": {},
        "events": {
            "max_per_day":          None,
            "max_per_week":         2,
            "max_per_month":        None,
            "max_per_year":         None,
            "upon_request_only":    False,
        },
        "organizations": {
            "max_per_day":          None,
            "max_per_week":         2,
            "max_per_month":        None,
            "max_per_year":         None,
            "upon_request_only":    True,
        },
        "places": {},
    },
    "MONTHLY": {
        "fare": 0,  # Cents.
        "attachments": {
            "documents": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "images": {
                "max_width":            900,
                "max_height":           600,
                "max_file_size":        102400,
                "max_per_event":        5,
                "max_per_organization": 5,
                "quality":              80,
            },
            "video": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "video_urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
        },
        "accounts": {},
        "events": {
            "max_per_day":          None,
            "max_per_week":         None,
            "max_per_month":        2,
            "max_per_year":         None,
            "upon_request_only":    False,
        },
        "organizations": {
            "max_per_day":          None,
            "max_per_week":         None,
            "max_per_month":        2,
            "max_per_year":         None,
            "upon_request_only":    True,
        },
        "places": {},
    },
    "YEARLY": {
        "fare": 0,  # Cents.
        "attachments": {
            "documents": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "images": {
                "max_width":            900,
                "max_height":           600,
                "max_file_size":        102400,
                "max_per_event":        5,
                "max_per_organization": 5,
                "quality":              80,
            },
            "video": {
                "max_file_size":        102400,
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
            "video_urls": {
                "max_per_event":        2,
                "max_per_organization": 2,
            },
        },
        "accounts": {},
        "events": {
            "max_per_day":          None,
            "max_per_week":         None,
            "max_per_month":        None,
            "max_per_year":         2,
            "upon_request_only":    False,
        },
        "organizations": {
            "max_per_day":          None,
            "max_per_week":         None,
            "max_per_month":        None,
            "max_per_year":         2,
            "upon_request_only":    True,
        },
        "places": {},
    },
}
SUBSCRIPTION_PLAN_DEFAULT = "DAILY"


###############################################################################
### AWS SETTINGS                                                            ###
###############################################################################


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################
CACHE_MIDDLEWARE_ALIAS = "db"
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = "local"


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################


###############################################################################
### DJANGO COMPRESSOR                                                       ###
###############################################################################
