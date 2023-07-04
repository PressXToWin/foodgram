from django_filters.rest_framework import FilterSet, filters

class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(favorites__user=self.request.user)