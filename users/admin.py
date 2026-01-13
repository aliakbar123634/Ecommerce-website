from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Admin panel me list view
    list_display = (
        "email",
        "full_name",
        "is_staff",
        "is_active",
        "created_at",
    )

    # Search bar
    search_fields = ("email", "full_name")

    # Filters right side
    list_filter = ("is_staff", "is_active", "created_at")

    ordering = ("email",)

    # User detail/edit form
    fieldsets = (
        ("Basic Info", {
            "fields": ("email", "full_name", "password"),
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions"),
        }),
        ("Important Dates", {
            "fields": ( "created_at",),
        }),
    )

    # Add user form (Add button)
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "full_name", "password1", "password2", "is_staff", "is_active"),
        }),
    )

    readonly_fields = ("created_at",)

    # filter_horizontal = ("groups", "user_permissions")
