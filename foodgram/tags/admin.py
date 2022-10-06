from django.contrib import admin

from .models import Tags


class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)


admin.site.register(Tags, TagsAdmin)
