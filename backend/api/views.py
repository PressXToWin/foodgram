from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer, RecipeCreateSerializer,
                             RecipeMainSerializer, RecipeShortSerializer,
                             TagSerializer, UserSubscribeSerializer)
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subscribe, Tag)

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

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
            favorite = get_object_or_404(
                Favorite,
                user=request.user,
                recipe=recipe
            )
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

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
                    {'error': 'Рецепт уже добавлен в список покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            cart = get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipe=recipe
            )
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    def items_in_cart(self, user):
        ingredients = RecipeIngredient.objects.filter(
            recipe__in_cart__user=user
        ).values('ingredient__name', 'ingredient__measurement_unit'
                 ).annotate(amount=Sum('amount'))
        answer = {}
        for item in ingredients:
            name = f'{item["ingredient__name"]}, '
            name += f'{item["ingredient__measurement_unit"]}'
            answer[name] = item['amount']
        return answer

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
        response['Content-Disposition'] = 'attachment; ' \
                                          'filename="shopping_list.txt"'
        return response


class ExtendedUserViewSet(UserViewSet):

    @action(detail=False, methods=['GET'])
    def subscriptions(self, request):
        user = request.user
        subscriptions = User.objects.filter(subscribing__user=user)
        pages = self.paginate_queryset(subscriptions)
        serializer = UserSubscribeSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['POST', 'DELETE'])
    def subscribe(self, request, id):
        author = User.objects.get(pk=id)
        serializer = UserSubscribeSerializer(
            author,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid()
        if request.method == 'POST':
            try:
                Subscribe.objects.create(user=request.user, author=author)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except IntegrityError:
                return Response(
                    {'error': 'Этот пользователь уже добавлен в подписки'},
                    status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            subscription = get_object_or_404(
                Subscribe,
                user=request.user,
                author=author
            )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = IngredientFilter
    pagination_class = None
