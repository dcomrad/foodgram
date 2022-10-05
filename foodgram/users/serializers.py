from rest_framework import serializers
from users.models import User, Followers
from recipes.core import SimpleRecipesSerializer


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False

        return Followers.objects.filter(user=user, author=obj).exists()


class UserSubscriptionSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')

        recipes_limit = request.GET.get('recipes_limit', '')
        recipes_limit = int(recipes_limit) if recipes_limit.isdigit() else None
        if recipes_limit is None:
            recipes = obj.recipes.all()
        else:
            recipes = obj.recipes.all()[:recipes_limit]

        return SimpleRecipesSerializer(instance=recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
