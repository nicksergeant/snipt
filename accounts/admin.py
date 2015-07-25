from django.contrib import admin

from accounts.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_pro', 'stripe_id', 'gittip_username',
                    'teams_beta_seen')
    list_filter = ['teams_beta_seen', 'teams_beta_applied']
    search_fields = ('user__username', 'gittip_username',)

admin.site.register(UserProfile, UserProfileAdmin)
