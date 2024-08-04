"""
(C) 2013-2024 Copycat Software, LLC. All Rights Reserved.
"""

import os
import os.path

from django.utils.translation import gettext_lazy as _

from decouple import config


###############################################################################
### PRODUCT VERSIONS                                                        ###
###############################################################################
PRODUCT_NAME = "2Remember"

# --- Versioning Strategy
#     <major>.<minor>.<patch>

VERSION_API = "v1"
VERSION_MAJOR = 0
VERSION_MINOR = 3
VERSION_PATCH = 1

PRODUCT_VERSION_NUM = f"v.{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}-RC1"


###############################################################################
### BASIC SETTINGS                                                          ###
###############################################################################
DEBUG = config("DEBUG", default=False)
DEBUG_TOOLBAR = True

# PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..",))

# We have 6 Types of Environments: "local", "dev", "test", "int", "staging", and "prod".
ENVIRONMENT = config("ENVIRONMENT", default="dev")

DJANGO_SETTINGS_MODULE = config("DJANGO_SETTINGS_MODULE", default="settings.dev")

ADMINS = (
    ("Artem Suvorov", "artem.suvorov@gmail.com"),
)
MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE":   config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME":     config("DB_NAME", default="sqlite.db"),
        "USER":     config("DB_USER", default=""),
        "PASSWORD": config("DB_PASSWORD", default=""),
        "HOST":     config("DB_HOST", default=""),
        "PORT":     config("DB_PORT", default=""),
        "OPTIONS": {
            # "autocommit": True,
        }
    }
}

DOMAIN_NAME = "2remember.live"
ALLOWED_HOSTS = ["*"]
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ["https://*.2remember.live"]
APPEND_SLASH = True

TIME_ZONE = "America/Los_Angeles"

LANGUAGE_CODE = "en-us"
LANGUAGES = (
    ("en",  _("English")),
    ("de",  _("Deutsch")),
    ("es",  _("Spanish")),
)

LOCALE_PATHS = (
    os.path.join(PROJECT_PATH, "locale"),
)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

ADMIN_MEDIA_PREFIX = "/static/admin/"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "staticserve")
STATICFILES_DIRS = (
    ("", f"{PROJECT_PATH}/static"),
)
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.DefaultStorageFinder",
)

SECRET_KEY = config("SECRET_KEY", default="@zew8t_wcz!qn9=8+hheltx@&b#!x@i6ores96lhbnobr3jp*c")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)

TEMPLATES = [
    {
        "BACKEND":  "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(PROJECT_PATH, "templates/"),
            os.path.join(PROJECT_PATH, "templates/emails/"),
            os.path.join(PROJECT_PATH, "templates/cyborg/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug":    DEBUG,
            # "loaders": [
            #     "django.template.loaders.filesystem.Loader",
            #     "django.template.loaders.app_directories.Loader",
            # ],
            "context_processors": [
                "django.template.context_processors.csrf",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",

                "url_tools.context_processors.current_url",

                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",

                "accounts.context_processors.signin_form",

                "events.context_processors.pb_event_choices",
                "events.context_processors.pb_participation_choices",

                "app.context_processors.pb_settings",
                "app.context_processors.pb_social_link_choices",
                "app.context_processors.pb_social_links",
                "app.context_processors.pb_supported_media",
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


###############################################################################
### DJANGO MIDDLEWARE CLASSES                                               ###
###############################################################################
MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
)

ROOT_URLCONF = "urls"

WSGI_APPLICATION = "wsgi.application"

INSTALLED_APPS = (
    # --- Django Apps
    "grappelli",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.contrib.messages",
    # "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",

    # --- 3rd Party Apps
    "adminsortable2",
    # "bootstrap3_datetime",
    "corsheaders",
    "ddcore",
    # "django_countries",
    "djangoformsetjs",
    # "djangosecure",
    # "jquery",
    # "papertrail",
    "rangefilter",
    # "sslserver",
    "storages",
    "timezone_field",
    "twitter_tag",
    "url_tools",

    # --- Project Apps
    "accounts",
    "api",
    "app",
    "blog",
    "events",
    "home",
    "invites",
    "organizations",
    "places",
    # "tests",
)

SESSION_SERIALIZER = "django.contrib.sessions.serializers.JSONSerializer"


###############################################################################
### DJANGO CACHING                                                          ###
###############################################################################
CACHES = {
    "default": {
        "BACKEND":  "django.core.cache.backends.dummy.DummyCache",
    },
    "some-other-cache": {
        "BACKEND":  "django.core.cache.backends.dummy.DummyCache",
    },
}


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################
LOGGING = {
    "version":                      1,
    "disable_existing_loggers":     False,
    "filters": {
        "require_debug_false": {
            "()":           "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()":           "django.utils.log.RequireDebugTrue",
        },
    },
    "formatters": {
        "simple": {
            "format":       "[{asctime}] {levelname} {message}",
            "datefmt":      "%Y-%m-%d %H:%M:%S",
            "style":        "{",
        },
        "verbose": {
            "format":       "[{asctime}] {levelname} [{name}.{funcName}:{lineno}] {message}",
            "datefmt":      "%Y-%m-%d %H:%M:%S",
            "style":        "{",
        },
        "json": {
            "()":           "app.logformat.VerboseJSONFormatter",
        },
    },
    "handlers": {
        "console": {
            "level":        "INFO",
            "filters": [
                "require_debug_true",
            ],
            "class":        "logging.StreamHandler",
            "formatter":    "simple",
        },
        "json_file": {
            "level":        "DEBUG",
            "class":        "logging.handlers.TimedRotatingFileHandler",
            "filename":     "logs/json.log",
            "when":         "midnight",
            "interval":     1,
            "backupCount":  7,
            "formatter":    "json",
        },
        "plain_file": {
            "level":        "INFO",
            "class":        "logging.handlers.TimedRotatingFileHandler",
            "filename":     "logs/plain.log",
            "when":         "midnight",
            "interval":     1,
            "backupCount":  7,
            "formatter":    "verbose",
        },
        "null": {
            "class":        "logging.NullHandler",
        },
        "mail_admins": {
            "level":        "ERROR",
            "filters": [
                "require_debug_false",
            ],
            "class":        "django.utils.log.AdminEmailHandler",
            "formatter":    "verbose",
        },
    },
    "loggers": {
        "": {
            "level":        "INFO",
            "handlers":     ["console", "json_file", "plain_file"],
            "propagate":    True,
        },
        "django": {
            "level":        "ERROR",
            "handlers":     ["console", "json_file", "plain_file"],
            "propagate":    True,
        },
        "django.request": {
            "level":        "ERROR",
            "handlers":     ["console", "json_file", "plain_file", "mail_admins"],
            "propagate":    True,
        },
        "py.warnings": {
            "handlers":     ["console", "json_file", "plain_file"],
        },
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)
AUTH_USER_MODEL = "ddcore.User"


###############################################################################
### CUSTOM PROJECT SETTINGS                                                 ###
###############################################################################
PAYPAL_SHARE_LINK = "https://www.paypal.com/donate/?business=LGZD2EA4KZYAG&no_recurring=0&item_name=Thank+you+for+your+Support.%0AYour+Donation+makes+a+Difference%21&currency_code=USD"

SELFREFLECTION_SUBMIT_DURATION_PERIOD = 7  # Days
PROFILE_COMPLETENESS_GRACE_PERIOD = 5  # Days

EVENT_TITLE_RESERVED_WORDS = [
    "near-you", "new", "dateless", "featured", "categories",
]
ORGANIZATION_TITLE_RESERVED_WORDS = [
    "directory", "create",
]


###############################################################################
### DJANGO BOWER                                                            ###
###############################################################################
INSTALLED_APPS += (
    "djangobower",
)
STATICFILES_FINDERS += (
    "djangobower.finders.BowerFinder",
)

BOWER_COMPONENTS_ROOT = os.path.join(PROJECT_PATH, "components/")
# BOWER_PATH = "/usr/local/bin/bower"
BOWER_INSTALLED_APPS = (
    # "awesome-bootstrap-checkbox",
    "bootpag",
    "bootstrap#5.3.3",
    "bootstrap-maxlength",
    # "bootstrap-rating",
    # "bootstrap-tagsinput",
    # "bx-slider.js",
    # "equalheight",
    "jquery#3.7.1",
    # "jquery.inputmask",
    "jquery-colorbox",
    "jquery-file-upload#10.32.0",
    "jquery-popup-overlay#1.6.0",
    # "jquery-shorten-js",
    # "jquery-sticky",
    "jquery-ui#1.12.1",
    # "jt.timepicker",
    "less.js#4.2.0",
    # "modernizr",
    "moment#2.30.1",
    "noty#3.1.4",
    "readmore-js",
    # "seiyria-bootstrap-slider",
    # "smooth-scroll.js",
    # "tablesorter",
    "underscore#1.13.6",
)


###############################################################################
### DJANGO CKEDITOR                                                         ###
###############################################################################
INSTALLED_APPS += (
    "ckeditor",
    "ckeditor_uploader",
)

AWS_QUERYSTRING_AUTH = False

CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_RESTRICT_BY_DATE = True
CKEDITOR_RESTRICT_BY_USER = False
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True

# CKEDITOR_CONFIGS = {
#     "default": {
#         "toolbar":      "full",
#         "height":       300,
#         "width":        300,
#     },
#     "awesome_ckeditor": {
#         "toolbar_CustomToolbarConfig": [
#             {
#                 "name":     "document",
#                 "items": [
#                     "Source", "-",
#                     "Save", "NewPage", "Preview", "Print", "-",
#                     "Templates",
#                 ]
#             },
#             {
#                 "name":     "clipboard",
#                 "items": [
#                     "Cut", "Copy", "Paste", "PasteText", "PasteFromWord", "-",
#                     "Undo", "Redo",
#                 ]
#             },
#             {
#                 "name":     "editing",
#                 "items": [
#                     "Find", "Replace", "-",
#                     "SelectAll",
#                 ]
#             },
#             {
#                 "name":     "forms",
#                 "items": [
#                     "Form", "Checkbox", "Radio", "TextField", "Textarea", "Select", "Button", "ImageButton", "HiddenField",
#                 ]
#             },
#             "/",
#             {
#                 "name":     "basicstyles",
#                 "items": [
#                     "Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript", "-",
#                     "RemoveFormat",
#                 ]
#             },
#             {
#                 "name":     "paragraph",
#                 "items": [
#                     "NumberedList", "BulletedList", "-",
#                     "Outdent", "Indent", "-",
#                     "Blockquote", "CreateDiv", "-",
#                     "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock", "-",
#                     "BidiLtr", "BidiRtl", "Language",
#                 ]
#             },
#             {
#                 "name":     "links",
#                 "items": [
#                     "Link", "Unlink", "Anchor",
#                 ]
#             },
#             {
#                 "name":     "insert",
#                 "items": [
#                     "Image", "Flash", "Table", "HorizontalRule", "Smiley", "SpecialChar", "PageBreak", "Iframe",
#                 ]
#             },
#             "/",
#             {
#                 "name":     "styles",
#                 "items": [
#                     "Styles", "Format", "Font", "FontSize",
#                 ]
#             },
#             {
#                 "name":     "colors",
#                 "items": [
#                     "TextColor", "BGColor",
#                 ]
#             },
#             {
#                 "name":     "tools",
#                 "items": [
#                     "Maximize", "ShowBlocks",
#                 ]
#             },
#             {
#                 "name":     "about",
#                 "items": [
#                     "About",
#                 ]
#             },
#         ],
#         "toolbar_CustomToolbarSmallConfig": [
#             {
#                 "name":     "document",
#                 "items": [
#                     "Source",
#                 ]
#             },
#             {
#                 "name":     "clipboard",
#                 "items": [
#                     "Undo", "Redo",
#                 ]
#             },
#             {
#                 "name":     "tools",
#                 "items": [
#                     "Maximize", "ShowBlocks", "About",
#                 ]
#             },
#             "/",
#             {
#                 "name":     "basicstyles",
#                 "items": [
#                     "Bold", "Italic", "Underline", "Strike", "Subscript", "Superscript", "-",
#                     "Outdent", "Indent", "-",
#                 ]
#             },
#             {
#                 "name":     "paragraph",
#                 "items": [
#                     "NumberedList", "BulletedList", "-",
#                     "Blockquote", "CreateDiv", "-",
#                     "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock",
#                 ]
#             },
#             {
#                 "name":     "insert",
#                 "items": [
#                     "Link", "Image", "Table", "HorizontalRule", "Smiley", "SpecialChar",
#                 ]
#             },
#             "/",
#             {
#                 "name":     "styles",
#                 "items": [
#                     "Styles", "Format", "Font", "FontSize", "TextColor", "BGColor",
#                 ]
#             },
#         ],
#         "toolbar":      "CustomToolbarSmallConfig",
#         # "skin":         "moono",
#         "height":       200,
#         "width":        "100%",
#         "tabSpaces":    4,
#     },
# }

IMAGE_QUALITY = 60
THUMBNAIL_SIZE = (300, 300)

X_FRAME_OPTIONS = "SAMEORIGIN"


###############################################################################
### DJANGO COMPRESSOR                                                       ###
###############################################################################
INSTALLED_APPS += (
    "compressor",
)
STATICFILES_FINDERS += (
    "compressor.finders.CompressorFinder",
)

COMPRESS_PRECOMPILERS = (
    ("text/coffeescript", "coffee --compile --stdio"),
    ("text/less", "lessc {infile} {outfile}"),
    ("text/x-sass", "sass {infile} {outfile}"),
    ("text/x-scss", "sass --scss {infile} {outfile}"),
    ("text/stylus", "stylus < {infile} > {outfile}"),
)
COMPRESS_CSS_FILTERS = [
    "compressor.filters.css_default.CssAbsoluteFilter",
    "compressor.filters.cssmin.CSSMinFilter",
    "compressor.filters.cssmin.CSSCompressorFilter",
]
COMPRESS_JS_FILTERS = [
    "compressor.filters.jsmin.JSMinFilter",
    "compressor.filters.jsmin.SlimItFilter",
]
COMPRESS_ENABLED = True


###############################################################################
### DJANGO EASY TIMEZONES                                                   ###
###############################################################################
# INSTALLED_APPS += (
#     "easy_timezones",
# )
# MIDDLEWARE += (
#     "easy_timezones.middleware.EasyTimezoneMiddleware",
# )
# GEOIP_DATABASE = os.path.join(PROJECT_PATH, "geoip/GeoLiteCity.dat")
# GEOIPV6_DATABASE = os.path.join(PROJECT_PATH, "geoip/GeoLiteCityv6.dat")


###############################################################################
### DJANGO GEOIP EXTRAS                                                     ###
###############################################################################
# INSTALLED_APPS += (
#     "geoip2_extras",
# )
MIDDLEWARE += (
    "geoip2_extras.middleware.GeoIP2Middleware",
)
GEOIP_PATH = os.path.join(PROJECT_PATH, "geoip/")
GEOIP2_EXTRAS_CACHE_NAME = "some-other-cache"
GEOIP2_EXTRAS_CACHE_TIMEOUT = 3600
GEOIP2_EXTRAS_ADD_RESPONSE_HEADERS = DEBUG


###############################################################################
### DJANGO GRAPPELLI                                                        ###
###############################################################################
GRAPPELLI_ADMIN_TITLE = "2Remember Admin"
GRAPPELLI_AUTOCOMPLETE_LIMIT = 25
# GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS
GRAPPELLI_SWITCH_USER = True
# GRAPPELLI_SWITCH_USER_ORIGINAL
# GRAPPELLI_SWITCH_USER_TARGET
# GRAPPELLI_CLEAN_INPUT_TYPES = False


###############################################################################
### DJANGO HAYSTACK                                                         ###
###############################################################################
# INSTALLED_APPS += (
#     "haystack",
# )

# HAYSTACK_CONNECTIONS = {
#     "default": {
#         "ENGINE":       "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine",
#         "URL":          "http://127.0.0.1:9200/",
#         "INDEX_NAME":   "haystack",
#     },
# }
# HAYSTACK_DEFAULT_OPERATOR = "AND"
# HAYSTACK_SEARCH_RESULTS_PER_PAGE = 50


###############################################################################
### DJANGO IMAGEKIT                                                         ###
###############################################################################
INSTALLED_APPS += (
    "imagekit",
)

IMAGEKIT_CACHEFILE_DIR = "CACHE/images"
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = "imagekit.cachefiles.backends.Simple"
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = "imagekit.cachefiles.strategies.JustInTime"
IMAGEKIT_CACHEFILE_NAMER = "imagekit.cachefiles.namers.hash"
IMAGEKIT_SPEC_CACHEFILE_NAMER = "imagekit.cachefiles.namers.source_name_as_path"


###############################################################################
### DJANGO MPTT                                                             ###
###############################################################################
# INSTALLED_APPS += (
#     "mptt",
# )

# MPTT_ADMIN_LEVEL_INDENT = 20


###############################################################################
### DJANGO MPTT ADMIN                                                       ###
###############################################################################
# INSTALLED_APPS += (
#     "django_mptt_admin",
# )


###############################################################################
### DJANGO PAGINATOR                                                        ###
###############################################################################
MAX_MEMBERS_PER_PAGE = 50
MAX_MEMBERS_PER_QUERY = 500

MAX_POSTS_PER_PAGE = 20
MAX_POSTS_PER_QUERY = 100

MAX_EVENTS_PER_PAGE = 25
MAX_EVENTS_PER_QUERY = 250

MAX_ORGANIZATIONS_PER_PAGE = 25
MAX_ORGANIZATIONS_PER_QUERY = 250


###############################################################################
### DJANGO PASSWORDS                                                        ###
###############################################################################
PASSWORD_MIN_LENGTH = 6         # Defaults to 6
PASSWORD_MAX_LENGTH = 30        # Defaults to None
PASSWORD_DICTIONARY = None
PASSWORD_MATCH_THRESHOLD = 0.9  # Defaults to 0.9, should be 0.0 - 1.0, where 1.0 means exactly the same.
PASSWORD_COMMON_SEQUENCES = []  # Should be a List of Strings. See `passwords/validators.py` for default
PASSWORD_COMPLEXITY = {         # You can omit any or all of these for no Limit for that particular Set
    "UPPER":    1,              # Uppercase
    "LOWER":    1,              # Lowercase
    "LETTERS":  1,              # Either uppercase or lowercase Letters
    "DIGITS":   1,              # Digits
    "SPECIAL":  1,              # Not alphanumeric, Space or punctuation Character
    "WORDS":    0,              # Words (alphanumeric Sequences, separated by a Whitespace or punctuation character)
}


###############################################################################
### DJANGO PHONE NUMBER FIELD                                               ###
###############################################################################
# INSTALLED_APPS += (
#     "phonenumber_field",
# )

# PHONENUMBER_DB_FORMAT = "INTERNATIONAL"


###############################################################################
### DJANGO REST FRAMEWORK                                                   ###
###############################################################################
INSTALLED_APPS += (
    "rest_framework",
    "rest_framework.authtoken",
)
REST_FRAMEWORK = {
    "DEFAULT_MODEL_SERIALIZER_CLASS":   "rest_framework.serializers.HyperlinkedModelSerializer",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.BrowsableAPIRenderer",
        "rest_framework.renderers.JSONRenderer",
        # "rest_framework_jsonp.renderers.JSONPRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),

    "TEST_REQUEST_DEFAULT_FORMAT":  "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.TemplateHTMLRenderer"
    ),
}


###############################################################################
### DJANGO ROSETTA                                                          ###
##############################################################################
INSTALLED_APPS += (
    "rosetta",
)

ROSETTA_MESSAGES_PER_PAGE = 20
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

YANDEX_TRANSLATE_KEY = "trnsl.1.1.20160321T202549Z.dc1425f58a3b7ddc.425ec99eb6632647ee447824f70d71f9dbaddb45"

AZURE_CLIENT_ID = None
AZURE_CLIENT_SECRET = None

ROSETTA_MESSAGES_SOURCE_LANGUAGE_CODE = "en"
ROSETTA_MESSAGES_SOURCE_LANGUAGE_NAME = "English"

ROSETTA_WSGI_AUTO_RELOAD = False
ROSETTA_UWSGI_AUTO_RELOAD = False

ROSETTA_EXCLUDED_APPLICATIONS = ()
ROSETTA_EXCLUDED_PATHS = ()

ROSETTA_REQUIRES_AUTH = True

ROSETTA_POFILE_WRAP_WIDTH = 0
ROSETTA_POFILENAMES = ("django.po", "djangojs.po")

ROSETTA_STORAGE_CLASS = "rosetta.storage.CacheRosettaStorage"
ROSETTA_ACCESS_CONTROL_FUNCTION = None

ROSETTA_LANGUAGE_GROUPS = False

ROSETTA_AUTO_COMPILE = True


###############################################################################
### DJANGO SEO                                                              ###
###############################################################################
# INSTALLED_APPS += (
#     "djangoseo",
# )


###############################################################################
### DJANGO SIMPLE CAPTCHA                                                   ###
###############################################################################
# INSTALLED_APPS += (
#     "captcha",
# )

# CAPTCHA_FONT_SIZE = 22
# CAPTCHA_BACKGROUND_COLOR = "#ffffff"
# CAPTCHA_FOREGROUND_COLOR = "#001100"
# CAPTCHA_PUNCTUATION = '''_"',.;:-'''
# CAPTCHA_TIMEOUT = 5  # Minutes
# CAPTCHA_LENGTH = 4  # Chars
# CAPTCHA_IMAGE_BEFORE_FIELD = True
# CAPTCHA_DICTIONARY_MIN_LENGTH = 0
# CAPTCHA_DICTIONARY_MAX_LENGTH = 99
# CAPTCHA_TEST_MODE = False


###############################################################################
### PYTHON/DJANGO SOCIAL AUTH                                               ###
###############################################################################
# INSTALLED_APPS += (
#     "social_django",
# )

# AUTHENTICATION_BACKENDS += (
#     "social_core.backends.facebook.FacebookAppOAuth2",
#     "social_core.backends.facebook.FacebookOAuth2",
#     "social_core.backends.twitter.TwitterOAuth",
#     "social_core.backends.linkedin.LinkedinOAuth2",
# )

# SESSION_SERIALIZER = "django.contrib.sessions.serializers.PickleSerializer"
# SESSION_COOKIE_AGE = 60 * 60 * 24 * 30  # One Month

LOGIN_URL = "/accounts/signin/"
LOGIN_REDIRECT_URL = "/accounts/my-profile/"
# LOGIN_ERROR_URL = "/login-error/"

# #SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/logged-in/"
# #SOCIAL_AUTH_LOGIN_ERROR_URL = "/login-error/"
# #SOCIAL_AUTH_LOGIN_URL = "/login-url/"
# #SOCIAL_AUTH_NEW_USER_REDIRECT_URL = "/new-users-redirect-url/"
# #SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = "/new-association-redirect-url/"
# #SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = "/account-disconnected-redirect-url/"
# #SOCIAL_AUTH_INACTIVE_USER_URL = "/inactive-user/"

# #SOCIAL_AUTH_USER_MODEL = "foo.bar.User"

# SOCIAL_AUTH_UUID_LENGTH = 16
# SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# SOCIAL_AUTH_SLUGIFY_USERNAMES = False
# SOCIAL_AUTH_CLEAN_USERNAMES = True

# SOCIAL_AUTH_COMPLETE_URL_NAME = "socialauth_complete"
# SOCIAL_AUTH_ASSOCIATE_URL_NAME = "socialauth_associate_complete"

# SOCIAL_AUTH_DEFAULT_USERNAME = lambda: random.choice([
#     "Darth_Vader", "Obi-Wan_Kenobi", "R2-D2", "C-3PO", "Yoda"
# ])
# SOCIAL_AUTH_CREATE_USERS = True

# SOCIAL_AUTH_PIPELINE = (
#     "social_core.pipeline.social_auth.social_details",
#     "social_core.pipeline.social_auth.social_uid",
#     "social_core.pipeline.social_auth.auth_allowed",
#     "social_core.pipeline.social_auth.social_user",
#     "social_core.pipeline.user.get_username",
#     "social_core.pipeline.mail.mail_validation",
#     "social_core.pipeline.social_auth.associate_by_email",
#     "social_core.pipeline.user.create_user",
#     "social_core.pipeline.social_auth.associate_user",
#     "social_core.pipeline.debug.debug",
#     "social_core.pipeline.social_auth.load_extra_data",
#     "social_core.pipeline.user.user_details",

#     "accounts.auth_pipelines.save_profile",
# )

# -----------------------------------------------------------------------------
# --- FACEBOOK
# -----------------------------------------------------------------------------
SOCIAL_AUTH_FACEBOOK_KEY = config("SOCIAL_AUTH_FACEBOOK_KEY", default="")
SOCIAL_AUTH_FACEBOOK_SECRET = config("SOCIAL_AUTH_FACEBOOK_SECRET", default="")
SOCIAL_AUTH_FACEBOOK_SCOPE = ["email", ]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields":   "id,name,email",
}

# -----------------------------------------------------------------------------
# --- TWITTER
# -----------------------------------------------------------------------------
TWITTER_OAUTH_TOKEN = config("TWITTER_OAUTH_TOKEN", default="")
TWITTER_OAUTH_SECRET = config("TWITTER_OAUTH_SECRET", default="")
TWITTER_CONSUMER_KEY = config("TWITTER_CONSUMER_KEY", default="")
TWITTER_CONSUMER_SECRET = config("TWITTER_CONSUMER_SECRET", default="")

SOCIAL_AUTH_TWITTER_KEY = TWITTER_CONSUMER_KEY
SOCIAL_AUTH_TWITTER_SECRET = TWITTER_CONSUMER_SECRET

# -----------------------------------------------------------------------------
# --- LINKEDIN
# -----------------------------------------------------------------------------
LINKEDIN_OAUTH_TOKEN = config("LINKEDIN_OAUTH_TOKEN", default="")
LINKEDIN_OAUTH_SECRET = config("LINKEDIN_OAUTH_SECRET", default="")
LINKEDIN_CONSUMER_KEY = config("LINKEDIN_CONSUMER_KEY", default="")
LINKEDIN_CONSUMER_SECRET = config("LINKEDIN_CONSUMER_SECRET", default="")
LINKEDIN_SCOPE = ["r_basicprofile", "r_emailaddress", ]
LINKEDIN_EXTRA_FIELD_SELECTORS = ["email-address", ]

# -----------------------------------------------------------------------------
# --- OAuth1 Settings.
# -----------------------------------------------------------------------------
SOCIAL_AUTH_LINKEDIN_KEY = LINKEDIN_CONSUMER_KEY
SOCIAL_AUTH_LINKEDIN_SECRET = LINKEDIN_CONSUMER_SECRET
SOCIAL_AUTH_LINKEDIN_SCOPE = LINKEDIN_SCOPE
SOCIAL_AUTH_LINKEDIN_FIELD_SELECTORS = LINKEDIN_EXTRA_FIELD_SELECTORS

# -----------------------------------------------------------------------------
# --- OAuth2 Settings.
# -----------------------------------------------------------------------------
SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = LINKEDIN_CONSUMER_KEY
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = LINKEDIN_CONSUMER_SECRET
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = LINKEDIN_SCOPE
SOCIAL_AUTH_LINKEDIN_OAUTH2_FIELD_SELECTORS = LINKEDIN_EXTRA_FIELD_SELECTORS


###############################################################################
### DJANGO TAGGIT                                                           ###
###############################################################################
INSTALLED_APPS += (
    "taggit",
    "taggit_templatetags2",
)

TAGGIT_CASE_INSENSITIVE = True
TAGGIT_STRIP_UNICODE_WHEN_SLUGIFYING = True
TAGGIT_TAGCLOUD_MIN = 1.0
TAGGIT_TAGCLOUD_MAX = 5.0
TAGGIT_LIMIT = 32
TAGGIT_TAG_LIST_ORDER_BY = "-num_times"
TAGGIT_TAG_CLOUD_ORDER_BY = "name"


###############################################################################
### DJANGO WHITE NOISE                                                      ###
###############################################################################
WHITENOISE_MAX_AGE = 31536000


###############################################################################
### MAILING                                                                 ###
###############################################################################
EMAIL_SENDER = "no-reply@2remember.live"
EMAIL_SUPPORT = "support@2remember.live"

# --- SendGrid Gateway
# EMAIL_BACKEND = "sgbackend.SendGridBackend"
# SENDGRID_API_KEY = ""


###############################################################################
### PROJECT PAGES TRIGGERS                                                  ###
###############################################################################


###############################################################################
### 2REMEMBER SOCIAL LINKS                                                  ###
###############################################################################
PB_SOCIAL_LINKS = {
    # --- On behalf of "artem.suvorov@gamil.com" / S1
    "PB_FACEBOOK":  "#",
    # --- On behalf of "support@2remember.live"    / S1
    "PB_TWITTER":   "https://x.com/2rememberlive",
    "PB_LINKEDIN":  "#",
    "PB_GOOGLE":    "#",
    "PB_PINTEREST": "#",
    # --- On behalf of "support@2remember.live"    / S1
    "PB_INSTAGRAM": "#",
    "PB_TUMBLR":    "#",
}


###############################################################################
### UPLOADING ATTACHMENTS                                                   ###
###############################################################################
UPLOADER_SETTINGS = {
    "default": {
        "MIME_TYPES_MAP": {
            "csv":  "text/csv",
            "doc":  "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "odt":  "application/vnd.oasis.opendocument.text",
            "pdf":  "application/pdf",
            "rtf":  "application/rtf",
            "txt":  "text/plain",
            "bmp":  "image/bmp",
            "gif":  "image/gif",
            "jpg":  "image/jpeg",
            "jpeg": "image/jpeg",
            "png":  "image/png",
            "tif":  "image/tiff",
            "tiff": "image/tiff",
            "webp": "image/webp",
        },
        "MAX_FILE_SIZE":    10485760,
        "MAX_FILE_NUMBER":  5,
        "AUTO_UPLOAD":      True,
    },
    "documents": {
        "MIME_TYPES_MAP": {
            "csv":  "text/csv",
            "doc":  "application/msword",
            "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "odt":  "application/vnd.oasis.opendocument.text",
            "pdf":  "application/pdf",
            "rtf":  "application/rtf",
            "txt":  "text/plain",
        },
        "MAX_FILE_SIZE":    10485760,
        "MAX_FILE_NUMBER":  5,
        "AUTO_UPLOAD":      True,
    },
    "images": {
        "MIME_TYPES_MAP": {
            "bmp":  "image/bmp",
            "gif":  "image/gif",
            "jpg":  "image/jpeg",
            "jpeg": "image/jpeg",
            "png":  "image/png",
            "tif":  "image/tiff",
            "tiff": "image/tiff",
            "webp": "image/webp",
        },
        "MAX_FILE_SIZE":    10485760,
        "MAX_FILE_NUMBER":  5,
        "AUTO_UPLOAD":      True,
    },
    "video": {
        "MIME_TYPES_MAP": {
            "avi":  "video/x-msvideo",
            "mp4":  "video/mp4",
            "mpg":  "video/mpeg",
            "mpeg": "video/mpeg",
            "ogv":  "video/ogg",
            "webm": "video/webm",
        },
        "MAX_FILE_SIZE":    10485760,
        "MAX_FILE_NUMBER":  5,
        "AUTO_UPLOAD":      True,
    },
    "audio": {
        "MIME_TYPES_MAP": {
            "aac":  "audio/aac",
            "mid":  "audio/midi",
            "midi": "audio/midi",
            "mp3":  "audio/mpeg",
            "ogv":  "audio/ogg",
            "wav":  "audio/wav",
            "weba": "audio/webm",
        },
        "MAX_FILE_SIZE":    10485760,
        "MAX_FILE_NUMBER":  5,
        "AUTO_UPLOAD":      True,
    }
}

SUPPORTED_DEFAULTS = [key for key, val in UPLOADER_SETTINGS["default"]["MIME_TYPES_MAP"].items()]
SUPPORTED_DEFAULTS_STR = ", ".join(SUPPORTED_DEFAULTS)
SUPPORTED_DEFAULTS_STR_EXT = ",".join([f".{key}" for key, val in UPLOADER_SETTINGS["default"]["MIME_TYPES_MAP"].items()])
SUPPORTED_DEFAULTS_STR_REG = "|".join([key for key, val in UPLOADER_SETTINGS["default"]["MIME_TYPES_MAP"].items()])

SUPPORTED_DOCUMENTS = [key for key, val in UPLOADER_SETTINGS["documents"]["MIME_TYPES_MAP"].items()]
SUPPORTED_DOCUMENTS_STR = ", ".join(SUPPORTED_DOCUMENTS)
SUPPORTED_DOCUMENTS_STR_EXT = ",".join([f".{key}" for key, val in UPLOADER_SETTINGS["documents"]["MIME_TYPES_MAP"].items()])
SUPPORTED_DOCUMENTS_STR_REG = "|".join([key for key, val in UPLOADER_SETTINGS["documents"]["MIME_TYPES_MAP"].items()])

SUPPORTED_IMAGES = [key for key, val in UPLOADER_SETTINGS["images"]["MIME_TYPES_MAP"].items()]
SUPPORTED_IMAGES_STR = ", ".join(SUPPORTED_IMAGES)
SUPPORTED_IMAGES_STR_EXT = ",".join([f".{key}" for key, val in UPLOADER_SETTINGS["images"]["MIME_TYPES_MAP"].items()])
SUPPORTED_IMAGES_STR_REG = "|".join([key for key, val in UPLOADER_SETTINGS["images"]["MIME_TYPES_MAP"].items()])


###############################################################################
### DJANGO SENTRY                                                           ###
###############################################################################
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn=config("SENTRY_DSN", default="https://b22808000322340efd7e59c981cbddd0@o4507562439802880.ingest.us.sentry.io/4507562447208448"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


###############################################################################
### DJANGO LOGGING                                                          ###
###############################################################################
MIDDLEWARE += (
    "app.middleware.DjangoRequestIDMiddleware",
    "app.middleware.DjangoLoggingMiddleware",
)
