from django.contrib import admin
from .models import ContentView


@admin.register(ContentView)
class ContentViewAdmin(admin.ModelAdmin):
    list_display  = ('content_type', 'object_id', 'view_token', 'viewed_at')
    list_filter   = ('content_type',)
    search_fields = ('object_id', 'view_token')
    readonly_fields = ('content_type', 'object_id', 'view_token', 'viewed_at')
    ordering = ('-viewed_at',)
