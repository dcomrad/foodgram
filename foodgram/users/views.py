from rest_framework import viewsets
from users.models import User
from users.serializers import UserSerializer


# class CustomUsersViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def get_permissions(self):
#         if self.action == "me":
#             return IsAuthenticated
#         return super().get_permissions()