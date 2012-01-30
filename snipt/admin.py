from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin

class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'last_login',
                    'date_joined', 'is_active', 'is_staff', 'api_key']
    list_filter = ['is_staff', 'is_superuser', 'is_active']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
