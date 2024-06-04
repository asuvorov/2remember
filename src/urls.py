"""
(C) 1995-2024 Copycat Software Corporation. All Rights Reserved.

The Copyright Owner has not given any Authority for any Publication of this Work.
This Work contains valuable Trade Secrets of Copycat, and must be maintained in Confidence.
Use of this Work is governed by the Terms and Conditions of a License Agreement with Copycat.

"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import (
    include,
    path,
    re_path)
from django.views.generic.base import TemplateView

# from rest_framework_swagger.views import get_swagger_view

# pylint: disable=import-error
from accounts.sitemap import AccountSitemap
from blog.sitemap import BlogPostSitemap
from events.sitemap import EventSitemap
from home.sitemap import HomeSitemap
from organizations.sitemap import OrganizationSitemap


admin.autodiscover()

# schema_view = get_swagger_view(title="SaneSide API")


sitemaps = {
    "accounts":         AccountSitemap,
    "blog":             BlogPostSitemap,
    "events":           EventSitemap,
    "home":             HomeSitemap,
    "organizations":    OrganizationSitemap,
}


urlpatterns = [
    re_path(r"", include("social_django.urls", namespace="social")),
    re_path(r"^ckeditor/", include("ckeditor_uploader.urls")),
    re_path(r"^grappelli/", include("grappelli.urls")),
    re_path(r"^admin/", admin.site.urls),
    # re_path(r"^captcha/", include("captcha.urls")),
    # re_path(r"^docs/", schema_view),
    re_path(r"^i18n/", include("django.conf.urls.i18n")),
    re_path(r"^rosetta/", include("rosetta.urls")),
    # re_path(r"^search/", include("haystack.urls")),
    re_path(r"^sitemap\.xml$", sitemap, {
            "sitemaps":     sitemaps,
        },
        name="django.contrib.sitemaps.views.sitemap"),

    re_path(r"^", include("home.urls")),
    re_path(r"^accounts/", include("accounts.urls")),
    re_path(r"^api/", include("api.urls")),
    re_path(r"^api/v1/", include("api.v1.urls")),
    re_path(r"^api/v2/", include("api.v2.urls")),
    re_path(r"^blog/", include("blog.urls")),
    re_path(r"^events/", include("events.urls")),
    re_path(r"^home/", include("home.urls")),
    re_path(r"^invites/", include("invites.urls")),
    re_path(r"^organizations/", include("organizations.urls")),

    path("humans.txt",TemplateView.as_view(template_name="cyborg/humans.txt", content_type="text/plain")),
    path("robots.txt",TemplateView.as_view(template_name="cyborg/robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = "app.views.handler400"
# handler403 = "app.views.handler403"
# handler404 = "app.views.handler404"
# handler500 = "app.views.handler500"

# if settings.DEBUG_TOOLBAR:
#     import debug_toolbar

#     urlpatterns += [
#         re_path(r"^debug/", include(debug_toolbar.urls)),
#     ]
