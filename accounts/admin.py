from django.contrib import admin

from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_pro', 'stripe_id',)
    search_fields = ('user__username',)

admin.site.register(UserProfile, UserProfileAdmin)
