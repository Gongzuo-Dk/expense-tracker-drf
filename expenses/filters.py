import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    date_after = django_filters.DateFilter(
        field_name='date',
        lookup_expr='gte'
    )
    date_before = django_filters.DateFilter(
        field_name='date',
        lookup_expr='lte'
    )
    min_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='gte'
    )
    max_amount = django_filters.NumberFilter(
        field_name='amount',
        lookup_expr='lte'
    )

    class Meta:
        model = Expense
        fields = ['category', 'date_after', 'date_before', 'min_amount', 'max_amount']