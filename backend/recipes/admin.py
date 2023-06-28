from django.contrib import admin

from recipes.models import (Recipe, Tag, Ingredient,
                            Subscribe, Favorite, ShoppingCart,
                            RecipeTag, RecipeIngredient)

admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Subscribe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredient)
