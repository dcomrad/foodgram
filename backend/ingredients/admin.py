from django.contrib import admin

from .models import Ingredients


class IngredientsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)


admin.site.register(Ingredients, IngredientsAdmin)
