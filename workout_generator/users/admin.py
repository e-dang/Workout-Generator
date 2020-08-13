from django.contrib.admin import site
from django.contrib.auth import admin

from .forms import UserCreationForm, UserChangeForm
from .models import User


class UserAdmin(admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('id', 'email', 'first_name', 'last_name')
    list_filter = ()

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    search_fields = ('id', 'email', 'first_name', 'last_name')
    ordering = ('id', 'email')


site.register(User, UserAdmin)
