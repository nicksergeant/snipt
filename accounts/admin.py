from django.contrib import admin

from accounts.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_pro', 'stripe_id', 'gittip_username',)
    search_fields = ('user__username', 'gittip_username',)

admin.site.register(UserProfile, UserProfileAdmin)
