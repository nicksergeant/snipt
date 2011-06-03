from django.contrib import admin

from snipts.models import Snipt

class SniptAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'tags', 'user', 'lexer', 'public', 'created', 'modified',)
    search_fields = ('title', 'user__username', 'tags', 'lexer',)
    ordering = ('created',)
    prepopulated_fields = {'slug': ('title',)}
    
admin.site.register(Snipt, SniptAdmin)
