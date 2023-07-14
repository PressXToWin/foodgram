from django.contrib import admin

from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            RecipeTag, ShoppingCart, Subscribe, Tag)


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'author',
    ]
    search_fields = ['name', 'author__username']
    list_filter = ['tags']
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'measurement_unit'
    ]
    search_fields = ['name']
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Subscribe)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)
admin.site.register(RecipeTag)
admin.site.register(RecipeIngredient)
