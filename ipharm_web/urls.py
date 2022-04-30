from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path

app_name = "ipharm"

admin.site.site_header = f"iPharm v{settings.APP_VERSION} Admin"
admin.site.site_title = f"Ipharm v{settings.APP_VERSION}"
admin.site.index_title = f"Welcome to iPharm Admin"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("ipharm.urls")),
    path("api/v1/", include("references.urls")),
    path("api/v1/", include("reports.urls")),
    path("api/v1/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("", lambda request: HttpResponse("Nothing to see here."), name="index"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.ENVIRONMENT == "development":
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
