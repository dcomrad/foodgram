from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ingredients.views import IngredientsViewSet
from recipes.views import RecipesViewSet, ShoppingCartView, FavoriteView
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

"""
    path('users/subscriptions/',
         SubscribeViewSet.as_view({'get': 'list'}), name='subscriptions'),
    path('recipes/download_shopping_cart/',
         DownloadCart.as_view({'get': 'download'}), name='download'),
    path('users/<users_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create',
                                   'delete': 'delete'}), name='subscribe'),
    path('recipes/<recipes_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create',
                                  'delete': 'delete'}), name='favorite'),
    path('recipes/<recipes_id>/shopping_cart/',
         CartViewSet.as_view({'post': 'create',
                              'delete': 'delete'}), name='cart'),
"""