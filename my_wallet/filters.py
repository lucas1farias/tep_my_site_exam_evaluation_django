

import django_filters
from .models import *


class TransactionFilter(django_filters.FilterSet):
    stock = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Transaction
        fields = ['stock']
