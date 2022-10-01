from rest_framework import viewsets
from recipes.models import Recipes
from recipes.serializers import ReadRecipesSerializer, WriteRecipesSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ReadRecipesSerializer
        else:
            return WriteRecipesSerializer
