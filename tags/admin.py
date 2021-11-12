from django.contrib import admin

from .models import Tag, TaggedItem

admin.site.register(Tag)
admin.site.register(TaggedItem)
