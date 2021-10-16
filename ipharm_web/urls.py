from django.conf import settings
from django.contrib import admin
from django.urls import include, path

app_name = "ipharm"

admin.site.site_header = f"iPharm v{settings.APP_VERSION} Admin"
admin.site.site_title = f"Ipharm v{settings.APP_VERSION}"
admin.site.index_title = f"Welcome to iPharm Admin"

urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/", include("ipharm.urls")),
    path("", admin.site.urls),
]
