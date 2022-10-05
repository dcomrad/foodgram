from rest_framework import viewsets
from ingredients.serializers import IngredientsSerializer
from recipes.models import Ingredients


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
