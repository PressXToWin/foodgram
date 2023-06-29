from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from recipes.models import (Recipe, Tag, Ingredient,
                            Subscribe, Favorite, ShoppingCart)

from api.serializers import (RecipeSerializer, TagSerializer, IngredientSerializer,
                            SubscribeSerializer, FavoriteSerializer, ShoppingCartSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
