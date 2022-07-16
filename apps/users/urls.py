from django.urls import path

from .views import logins, user

app_name = "users"

urlpatterns = [
    path("user/", user.UserView.as_view(), name="user"),
    path("login_basic/", logins.LoginBasic.as_view(), name="login_basic"),
]
