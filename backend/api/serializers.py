from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (Recipe, Tag, Ingredient,
                            Subscribe, Favorite, ShoppingCart,
                            RecipeIngredient)


User = get_user_model()


class UserMainSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True,
        max_length=50
    )
    last_name = serializers.CharField(
        required=True,
        max_length=50
    )

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        )
        model = User


class UserViewSerializer(UserMainSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if not self.context.get('request').user.is_authenticated or self.context.get('request').user == obj:
            return False
        subscribe = Subscribe.objects.filter(user=self.context.get('request').user, author=obj)
        return subscribe.exists()

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class SubscribeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True, source='recipe')
    author = UserViewSerializer()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return False
        favorite = Favorite.objects.filter(user=self.context.get('request').user, recipe=obj)
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return False
        cart = ShoppingCart.objects.filter(user=self.context.get('request').user, recipe=obj)
        return cart.exists()

    class Meta:
        model = Recipe
        fields = '__all__'
