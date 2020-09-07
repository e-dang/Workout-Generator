from django_filters import rest_framework as filters
from .models import Equipment
from django.contrib.postgres.fields import ArrayField


class EquipmentFilter(filters.FilterSet):
    class Meta:
        model = Equipment
        fields = {
            'owner': ['exact'],
            'name': ['iexact'],
            'snames': ['icontains']
        }
        filter_overrides = {
            ArrayField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            }
        }
