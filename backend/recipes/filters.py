from django_filters.rest_framework import FilterSet, filters


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='filter_is_in_shopping_cart')

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(favorites__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(in_cart__user=self.request.user)
