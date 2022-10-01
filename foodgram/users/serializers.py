from rest_framework import serializers
from users.models import User, Followers


class BaseUserValidation:
    @staticmethod
    def validate_username(username):
        if username == 'me':
            raise serializers.ValidationError(
                'Недопустимое имя пользователя'
            )
        return username


class UserSerializer(BaseUserValidation, serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        read_only_fields = ['id']

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False

        return Followers.objects.filter(user=user, author=obj).exists()
