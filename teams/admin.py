from django.contrib import admin
from teams.models import Team


class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created", "modified")
    ordering = ("-created",)


admin.site.register(Team, TeamAdmin)
