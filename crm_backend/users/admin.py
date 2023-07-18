from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, User


class CategoryInline(admin.StackedInline):
    model = Category


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [CategoryInline, ]
    list_display = ('email', 'first_name', 'last_name',
                    'role', 'category', 'is_staff')
    list_filter = ('email', 'first_name', 'last_name', 'role', 'category')
    search_fields = ('email', 'first_name', 'last_name', )
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name',)
    empty_value_display = '-пусто-'
