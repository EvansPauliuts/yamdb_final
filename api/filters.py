import django_filters as filters

from .models import Categories, Genres, Titles


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    category = filters.ModelChoiceFilter(
        queryset=Categories.objects.all(),
        to_field_name='slug'
    )

    genre = filters.ModelChoiceFilter(
        queryset=Genres.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Titles
        fields = ('name', 'year', 'category', 'genre')
