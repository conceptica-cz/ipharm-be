from django.urls import path

from .views import user

app_name = "users"

urlpatterns = [
    path("user/", user.UserView.as_view(), name="user"),
]
