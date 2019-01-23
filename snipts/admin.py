from django.contrib import admin
from snipts.models import Favorite, Snipt, SniptLogEntry


class SniptAdmin(admin.ModelAdmin):
    readonly_fields = ("last_user_saved", "user")
    list_display = (
        "title",
        "slug",
        "views",
        "favs",
        "user",
        "lexer",
        "public",
        "blog_post",
        "created",
        "modified",
        "publish_date",
    )
    list_filter = ("blog_post",)
    search_fields = ("title", "slug", "user__username", "lexer", "id", "key")
    ordering = ("-created",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Snipt, SniptAdmin)


class SniptLogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ("snipt", "user")
    list_display = ("snipt_name", "user", "created", "modified")


admin.site.register(SniptLogEntry, SniptLogEntryAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    readonly_fields = ("snipt", "user")
    list_display = ("snipt", "user", "created")
    search_fields = ("snipt", "user")
    ordering = ("-created",)


admin.site.register(Favorite, FavoriteAdmin)
