from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ("username", "is_staff", "is_active", "is_system")
    list_filter = (
        "is_staff",
        "is_system",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (None, {"fields": ("first_name", "last_name", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_system",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Settings", {"fields": ("hospitals", "ambulances")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_system",
                ),
            },
        ),
    )
    search_fields = ("username",)
    ordering = ("username",)
