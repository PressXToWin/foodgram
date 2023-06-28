from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                       SubscribeViewSet, FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('recipes', RecipeViewSet, basename='recipes')
v1_router.register('tags', TagViewSet, basename='tags')
v1_router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('', include('djoser.urls.jwt')),
    path('', include('djoser.urls')),
]
