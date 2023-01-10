"""Define URL Paths."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import (
    include,
    re_path)

from rest_framework_swagger.views import get_swagger_view

# pylint: disable=import-error
from accounts.sitemap import AccountSitemap
from blog.sitemap import BlogPostSitemap
from events.sitemap import EventSitemap
from home.sitemap import HomeSitemap
from organizations.sitemap import OrganizationSitemap


admin.autodiscover()

schema_view = get_swagger_view(title="SaneSide API")


sitemaps = {
    "accounts":         AccountSitemap,
    "blog":             BlogPostSitemap,
    "events":           EventSitemap,
    "home":             HomeSitemap,
    "organizations":    OrganizationSitemap,
}


urlpatterns = [
    # re_path(r"", include("social_django.urls", namespace="social")),
    # re_path(r"^", include("cyborg.urls")),

    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    # re_path(r"^grappelli/", include("grappelli.urls")),
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^captcha/", include("captcha.urls")),
    re_path(r"^docs/", schema_view),
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    # re_path(r"^rosetta/", include("rosetta.urls")),
    re_path(r"^search/", include("haystack.urls")),
    re_path(r"^sitemap\.xml$", sitemap, {
            "sitemaps":     sitemaps,
        },
        name="django.contrib.sitemaps.views.sitemap"),

    re_path(r"^", include("home.urls")),
    re_path(r"^accounts/", include("accounts.urls")),
    re_path(r"^api/v1/", include("api.v1.urls")),
    re_path(r"^api/v2/", include("api.v2.urls")),
    re_path(r"^blog/", include("blog.urls")),
    re_path(r"^events/", include("events.urls")),
    re_path(r"^home/", include("home.urls")),
    re_path(r"^invites/", include("invites.urls")),
    re_path(r"^organizations/", include("organizations.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = "app.views.handler400"
# handler403 = "app.views.handler403"
# handler404 = "app.views.handler404"
# handler500 = "app.views.handler500"

if settings.DEBUG_TOOLBAR:
    import debug_toolbar

    urlpatterns += [
        re_path(r"^debug/", include(debug_toolbar.urls)),
    ]
