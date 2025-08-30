from django.contrib import admin

from accounts.models import User, UserToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ('access_token',)
