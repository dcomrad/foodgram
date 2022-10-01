from rest_framework import serializers
from recipes.models import Recipes
from tags.serializers import TagsSerializer
from users.serializers import UserSerializer
from recipes.models import IngredientsRecipes, Favorites, ShoppingCart


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


# class WriteIngredientsRecipesSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(source='ingredient.id')
#
#     class Meta:
#         model = IngredientsRecipes
#         fields = ('id', 'amount')

# *****************************************************************


class RecipesSerializer(serializers.ModelSerializer):
    ingredients = IngredientsRecipesSerializer(source='recipe_ingredients',
                                               many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return Favorites.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False

        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class ReadRecipesSerializer(RecipesSerializer):
    """Сериализатор рецептов для метода GET"""
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)


class WriteRecipesSerializer(RecipesSerializer):
    """Сериализатор рецептов для метода POST"""
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

