from rest_framework import serializers
from django.shortcuts import get_object_or_404

from recipes.models import Recipes, IngredientsRecipes, Favorites, ShoppingCart, TagsRecipes
from tags.models import Tags
from tags.serializers import TagsSerializer
from users.serializers import UserSerializer
from ingredients.models import Ingredients


class IngredientsRecipesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )

    class Meta:
        model = IngredientsRecipes
        fields = ('id', 'name', 'measurement_unit', 'amount')


class BaseRecipesSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    ingredients = IngredientsRecipesSerializer(source='recipe_ingredients',
                                               many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

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


class ReadRecipesSerializer(BaseRecipesSerializer):
    """Сериализатор рецептов для метода GET"""
    tags = TagsSerializer(many=True, read_only=True)


class WriteRecipesSerializer(BaseRecipesSerializer):
    """Сериализатор рецептов для метода POST"""
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tags.objects.all())
    # image = Base64Field

    def validate(self, attrs):
        return attrs

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            message = 'Тэги не должны повторяться'
            raise serializers.ValidationError(message)
        return tags

    def validate_ingredients(self, ingredients):
        ingredient_ids = set()
        for ingredient in ingredients:
            get_object_or_404(Ingredients, id=ingredient['ingredient']['id'])
            ingredient_ids.add(ingredient['ingredient']['id'])
            if ingredient['amount'] <= 0:
                message = 'Количество ингредиента должно быть положительным'
                raise serializers.ValidationError(message)
        if len(ingredients) != len(ingredient_ids):
            message = 'Ингредиенты не должны повторяться'
            raise serializers.ValidationError(message)

        return ingredients

    def create(self, validated_data):
        recipe = Recipes.objects.create(
                author=self.context.get('request').user,
                name=validated_data.get('name'),
                image=validated_data.get('image'),
                text=validated_data.get('text'),
                cooking_time=validated_data.get('cooking_time'),
            )

        tags = validated_data.pop('tags')
        for tag in tags:
            TagsRecipes.objects.create(recipe_id=recipe.id, tag_id=tag.id)

        ingredients = validated_data.pop('recipe_ingredients')
        for ingredient in ingredients:
            IngredientsRecipes.objects.create(
                ingredient_id=ingredient['ingredient']['id'],
                recipe_id=recipe.id,
                amount=ingredient['amount']
            )

        return recipe

    def update(self, instance, validated_data):
        pass
