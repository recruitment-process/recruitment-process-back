from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Переопределены поля формы для исключения поля username."""

    model = User

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "patronymic",
                    "role",
                    "category",
                    "telegram",
                    "photo",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    readonly_fields = (
        "last_login",
        "date_joined",
    )
    list_display = ("email", "first_name", "last_name", "role", "category", "is_staff")
    list_filter = ("email", "first_name", "last_name", "role", "category")
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    empty_value_display = "-пусто-"
    ordering = ("-id",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
    empty_value_display = "-пусто-"
    ordering = ("name",)
