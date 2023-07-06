from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS

from recipes.filters import RecipeFilter
from recipes.models import (Recipe, Tag, Ingredient,
                            Subscribe, Favorite, ShoppingCart, RecipeIngredient)

from api.serializers import (RecipeMainSerializer, TagSerializer, IngredientSerializer,
                             SubscribeSerializer, FavoriteSerializer, ShoppingCartSerializer, RecipeCreateSerializer,
                             RecipeShortSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeMainSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == 'POST':
            try:
                Favorite.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data)
            except IntegrityError:
                return Response(
                    {'error': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            favorite = get_object_or_404(Favorite, user=request.user, recipe=recipe)
            favorite.delete()

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = Recipe.objects.get(pk=pk)
        serializer = RecipeShortSerializer(recipe)
        if request.method == 'POST':
            try:
                ShoppingCart.objects.create(user=request.user, recipe=recipe)
                return Response(serializer.data)
            except IntegrityError:
                return Response(
                    {'error': 'Рецепт уже добавлен в избранное'},
                    status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cart = get_object_or_404(ShoppingCart, user=request.user, recipe=recipe)
            cart.delete()

    def items_in_cart(self, user):
        ingredients = RecipeIngredient.objects.filter(recipe__in_cart__user=user)
        answer_dict = {}
        for item in ingredients:
            name = f'{item.ingredient.name}, {item.ingredient.measurement_unit}'
            if name not in answer_dict:
                answer_dict[name] = 0
            answer_dict[name] += item.amount
        return answer_dict

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        cart_data = self.items_in_cart(request.user)
        answer_text = 'Foodgram - продуктовый помощник.\n\n\n'
        answer_text += 'Список покупок: \n\n'
        for key, value in cart_data.items():
            answer_text += f'{key} - {value} \n'
        response = HttpResponse(
            answer_text,
            content_type='text/plain',
            status=status.HTTP_200_OK)
        response['Content-Disposition'] = 'attachment; filename="shopping_list.txt"'
        return response



class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class SubscribeViewSet(viewsets.ModelViewSet):
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer


class ShoppingCartViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
