from rest_framework import serializers
from recipes.models import Recipes


class SimpleRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = fields

