from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from users.models import Followers, User
from users.serializers import UserSubscriptionSerializer


class CustomUsersViewSet(UserViewSet):
    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return super().get_permissions()


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @staticmethod
    def not_found():
        message = 'Такого пользователя не существует'
        return Response(data=f"{{'errors': '{message}'}}",
                        status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def bad_request(message):
        return Response(data=f"{{'errors': '{message}'}}",
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        followers = (follow.author for follow in request.user.follower.all())
        paginator = self.pagination_class()
        paginated = paginator.paginate_queryset(queryset=list(followers),
                                                request=request)

        serializer = UserSubscriptionSerializer(
            instance=paginated, many=True, context={'request': request}
        )
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, user_id):
        user = User.objects.filter(id=user_id)
        if not user.exists():
            return self.not_found()

        if request.user.id == user_id:
            return self.bad_request('Нельзя подписаться на самого себя')

        if Followers.objects.filter(user=request.user,
                                    author_id=user_id).exists():
            return self.bad_request('Такая подписка уже существует')

        Followers.objects.create(user=request.user, author_id=user_id)

        serializer = UserSubscriptionSerializer(
            instance=user.first(), context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        if not User.objects.filter(id=user_id).exists():
            return self.not_found()

        deleted, _ = Followers.objects.filter(user=request.user,
                                              author_id=user_id).delete()
        if not deleted:
            return self.bad_request('Вы не подписаны на этого пользователя')

        return Response(status=status.HTTP_204_NO_CONTENT)
