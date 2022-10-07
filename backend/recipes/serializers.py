from django.shortcuts import get_object_or_404
from ingredients.models import Ingredients
from recipes.core import Base64ImageField
from recipes.models import (Favorites, IngredientsRecipes, Recipes,
                            ShoppingCart, TagsRecipes)
from rest_framework import serializers
from tags.models import Tags
from tags.serializers import TagsSerializer
from users.serializers import UserSerializer


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
    image = Base64ImageField()

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

    def validate_tags(self, tags):
        if len(tags) != len(set(tags)):
            message = 'Тэги не должны повторяться'
            raise serializers.ValidationError(message)
        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            message = 'Добавьте в рецепт хотя бы один ингредиент'
            raise serializers.ValidationError(message)

        ingredient_ids = set()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredient').get('id') if (
                ingredient.get('ingredient')) else None
            get_object_or_404(Ingredients, id=ingredient_id)
            ingredient_ids.add(ingredient_id)
            if ingredient['amount'] <= 0:
                message = 'Количество ингредиента должно быть положительным'
                raise serializers.ValidationError(message)
        if len(ingredients) != len(ingredient_ids):
            message = 'Ингредиенты не должны повторяться'
            raise serializers.ValidationError(message)

        return ingredients

    @staticmethod
    def create_tags_and_ingredients(recipe, tags, ingredients):
        tag_objs = list(
            TagsRecipes(recipe_id=recipe.id, tag_id=tag.id) for tag in tags
        )
        TagsRecipes.objects.bulk_create(tag_objs)

        ingredient_objs = list(
            IngredientsRecipes(
                ingredient_id=ingredient['ingredient']['id'],
                recipe_id=recipe.id,
                amount=ingredient['amount']
            ) for ingredient in ingredients
        )
        IngredientsRecipes.objects.bulk_create(ingredient_objs)

    def create(self, validated_data):
        recipe = Recipes.objects.create(
            author=self.context.get('request').user,
            name=validated_data.get('name'),
            image=validated_data.get('image'),
            text=validated_data.get('text'),
            cooking_time=validated_data.get('cooking_time'),
        )

        self.create_tags_and_ingredients(
            recipe,
            validated_data.pop('tags'),
            validated_data.pop('recipe_ingredients')
        )

        return recipe

    def update(self, instance, validated_data):
        TagsRecipes.objects.filter(recipe=instance).delete()
        IngredientsRecipes.objects.filter(recipe=instance).delete()

        self.create_tags_and_ingredients(
            instance,
            validated_data.pop('tags'),
            validated_data.pop('recipe_ingredients')
        )

        return super().update(instance, validated_data)
