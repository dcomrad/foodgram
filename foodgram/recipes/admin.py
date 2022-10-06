from django.contrib import admin

from .models import Favorites, Recipes, ShoppingCart


class RecipesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'author', 'cooking_time',
                    'favorites_amount')
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')

    def favorites_amount(self, obj):
        return Favorites.objects.filter(recipe=obj).count()

    favorites_amount.short_description = 'Число добавлений рецепта в избранное'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    list_filter = ('user', 'recipe')


admin.site.register(Recipes, RecipesAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Favorites, FavoritesAdmin)
