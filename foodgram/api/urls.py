from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ingredients.views import IngredientsViewSet
from recipes.views import RecipesViewSet
from tags.views import TagsViewSet


app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register(r'recipes', RecipesViewSet, basename='recipes')
router_v1.register(r'tags', TagsViewSet, basename='tags')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    # path('v1/recipes/<pk:int>/shopping_cart/', )
]

