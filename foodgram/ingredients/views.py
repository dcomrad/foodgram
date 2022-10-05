from rest_framework import viewsets
from ingredients.serializers import IngredientsSerializer
from recipes.models import Ingredients
from django_filters.rest_framework import DjangoFilterBackend


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('name',)
