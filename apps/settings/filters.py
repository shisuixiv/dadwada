import django_filters

from apps.settings.models import Book

class BookFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_year = django_filters.NumberFilter(field_name='published_year', lookup_expr='gte')
    max_year = django_filters.NumberFilter(field_name='published_year', lookup_expr='lte')


    class Meta:
        model = Book
        fields = ["author", "genre", "published_year", "min_price", "max_price", 'min_year', 'max_year']