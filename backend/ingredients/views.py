from api.filters import IngredientSearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ingredients.serializers import IngredientsSerializer
from recipes.models import Ingredients
from rest_framework import viewsets


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend, IngredientSearchFilter)
    search_fields = ('^name',)
