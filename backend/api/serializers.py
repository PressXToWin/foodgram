from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Subscribe, Tag)

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
        if not self.context.get('request').user.is_authenticated \
                or self.context.get('request').user == obj:
            return False
        subscribe = Subscribe.objects.filter(
            user=self.context.get('request').user,
            author=obj
        )
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


class UserSubscribeSerializer(UserViewSerializer):
    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = User

    def get_recipes_count(self, obj):
        recipes_count = obj.recipes.count()
        return recipes_count

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        serializer = RecipeShortSerializer(recipes, many=True)
        return serializer.data

    def validate(self, data):
        if Subscribe.objects.filter(
                user=data['user'],
                author=data['author']
        ).exists():
            raise serializers.ValidationError(
                'Этот пользователь уже добавлен в подписки'
            )
        return data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeMainSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientInRecipeSerializer(many=True, source='recipe')
    author = UserViewSerializer(default=serializers.CurrentUserDefault())
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(max_length=None)

    def get_is_favorited(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return False
        favorite = Favorite.objects.filter(
            user=self.context.get('request').user,
            recipe=obj
        )
        return favorite.exists()

    def get_is_in_shopping_cart(self, obj):
        if not self.context.get('request').user.is_authenticated:
            return False
        cart = ShoppingCart.objects.filter(
            user=self.context.get('request').user,
            recipe=obj
        )
        return cart.exists()

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCreateSerializer(RecipeMainSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientInRecipeSerializer(many=True)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'tags' in validated_data:
            instance.tags.clear()
            instance.tags.set(validated_data.pop('tags'))
        if 'ingredients' in validated_data:
            instance.ingredients.clear()
            self.create_ingredients(
                validated_data.pop('ingredients'),
                instance
            )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeMainSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class RecipeShortSerializer(serializers.ModelSerializer):
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
