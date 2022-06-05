from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ['username', 'is_staff']

    fieldsets = (
        ('ユーザー情報', {'fields': ('username', 'loginid', 'password', 'profile_image', 'create_at', 'update_at')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')})
    )

    add_fieldsets = (
        ('ユーザー情報', {
            'fields': ('username', 'loginid', 'password', 'confirm_password')
        }),
    )

admin.site.register(User, CustomizeUserAdmin)