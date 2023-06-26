from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=50)


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
    text = models.TextField()
    cooking_time = models.PositiveIntegerField()


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
