import os
from wsgiref.util import FileWrapper

from django.conf import settings
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.core import SimpleRecipesSerializer
from recipes.models import Favorites, IngredientsRecipes, Recipes, ShoppingCart
from recipes.serializers import ReadRecipesSerializer, WriteRecipesSerializer

from .permissions import IsAdminOrOwner


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Вьюсет обработки рецептов
    """
    ALLOWABLE_ENUM = ['0', '1']
    FILEPATH = os.path.join(settings.MEDIA_ROOT, 'recipes', 'cart')

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('author',)

    def get_queryset(self):
        """
        Фильтрация рецептов по параметрам GET-запроса
        """
        def get_request_param(param):
            result = self.request.GET.get(param, '')
            result = int(result) if (
                result.isdigit() and result in self.ALLOWABLE_ENUM) else None
            return result

        is_favorited = get_request_param('is_favorited')
        is_in_shopping_cart = get_request_param('is_in_shopping_cart')
        tag_slugs = self.request.GET.getlist('tags', [])

        queryset = Recipes.objects.all()

        if tag_slugs:
            queryset = queryset.filter(tags__slug__in=tag_slugs).distinct()

        if is_favorited:
            favorited_recipes = self.request.user.favorites.all().values_list(
                'recipe', flat=True
            )
            queryset = queryset.filter(id__in=favorited_recipes)

        if is_in_shopping_cart:
            in_cart_recipes = self.request.user.cart.all().values_list(
                'recipe', flat=True
            )
            queryset = queryset.filter(id__in=in_cart_recipes)

        return queryset

    def get_permissions(self):
        if self.action == 'download_shopping_cart':
            return [IsAuthenticated()]
        if self.action in ['create', 'partial_update', 'destroy']:
            return [IsAdminOrOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadRecipesSerializer
        else:
            return WriteRecipesSerializer

    @action(detail=False)
    def download_shopping_cart(self, request):
        """
        Функция обработки запроса скачивания списка ингредиентов, добавленных
        в корзину. Выгружает в файл в .txt формате
        """
        ingredients = IngredientsRecipes.objects.filter(
            recipe__cart__user=request.user).values(
                'ingredient__name', 'ingredient__measurement_unit').order_by(
                    'ingredient__name').annotate(amount=Sum('amount'))

        if not os.path.exists(self.FILEPATH):
            os.makedirs(self.FILEPATH)
        unique_filename = f'Список покупок {self.request.user.username}.txt'
        filename = os.path.join(self.FILEPATH, unique_filename)

        with open(filename, mode='w', encoding='utf-8') as file:
            for ingredient in ingredients:
                name = ingredient['ingredient__name']
                measurement_unit = ingredient['ingredient__measurement_unit']
                amount = ingredient['amount']
                file.write(f'{name} ({measurement_unit}): {amount}\n')

        file = open(filename, encoding='utf-8')
        return FileResponse(FileWrapper(file), content_type='text/plain',
                            filename=filename)


class BaseShoppingCartFavoriteView(APIView):
    model = None
    where = ''
    permission_classes = [IsAuthenticated]

    @staticmethod
    def bad_request(message):
        return Response(data=f"{{'errors': '{message}'}}",
                        status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, recipe_id):
        if not Recipes.objects.filter(id=recipe_id).exists():
            return self.bad_request('Такого рецепта не существует')

        if self.model.objects.filter(user=request.user,
                                     recipe_id=recipe_id).exists():
            return self.bad_request(f'Такой рецепт уже есть в {self.where}')

        cart = self.model.objects.create(user=request.user,
                                         recipe_id=recipe_id)
        serializer = SimpleRecipesSerializer(instance=cart.recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        if not Recipes.objects.filter(id=recipe_id).exists():
            return self.bad_request('Такого рецепта не существует')

        deleted, _ = self.model.objects.filter(user=request.user,
                                               recipe_id=recipe_id).delete()
        if not deleted:
            return self.bad_request(f'Такого рецепта нет в {self.where}')

        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartView(BaseShoppingCartFavoriteView):
    model = ShoppingCart
    where = 'корзине'


class FavoriteView(BaseShoppingCartFavoriteView):
    model = Favorites
    where = 'избранном'
