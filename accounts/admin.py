from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . forms import SignUpForm, LoginForm, PwdResetForm, UserEditForm
from . models import CustomUser, Profile


class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = SignUpForm
    model = CustomUser
    list_display = ('first_name','last_name','email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)