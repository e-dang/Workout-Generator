from django.contrib.admin import site
from django.contrib.auth import admin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password', 'is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('id', 'email', 'first_name', 'last_name')
    ordering = ('id', 'email')


site.register(User, UserAdmin)
