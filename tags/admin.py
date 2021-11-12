from django.contrib import admin

from .models import Tag, TaggedItem


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Custom admin for managing Tags."""

    search_fields = ["label"]
