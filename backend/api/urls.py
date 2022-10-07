from django.urls import include, path
from ingredients.views import IngredientsViewSet
from recipes.views import FavoriteView, RecipesViewSet, ShoppingCartView
from rest_framework.routers import DefaultRouter
from tags.views import TagsViewSet
from users.views import CustomUsersViewSet, SubscriptionView

app_name = 'api'

router = DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'users', CustomUsersViewSet, basename='users')

urlpatterns = [
    path('users/subscriptions/', SubscriptionView.as_view()),
    path('users/<int:user_id>/subscribe/', SubscriptionView.as_view()),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
    path('recipes/<int:recipe_id>/favorite/', FavoriteView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
