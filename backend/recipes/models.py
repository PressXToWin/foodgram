from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_name_unit'
            )
        ]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=8)
    slug = models.SlugField(unique=True)


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, related_name='recipes', through='RecipeTag')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', through='RecipeIngredient')
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    name = models.CharField(max_length=200)
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='media/',
        blank=True
    )
    text = models.TextField(blank=True)
    cooking_time = models.PositiveIntegerField(default=0)


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)


class Subscribe(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing'
    )


class Favorite(models.Model):
    """Модель избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favoriter'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='in_cart'
    )
