from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from ingredients.serializers import IngredientsSerializer
from recipes.models import Ingredients


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [AllowAny]
