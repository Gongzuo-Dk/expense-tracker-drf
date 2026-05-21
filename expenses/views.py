from django.db.models import Sum, Count, Avg
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this category.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this category.")
        instance.delete()


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from .filters import ExpenseFilter


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = ExpenseFilter
    ordering_fields = ['date', 'amount', 'created_at']
    ordering = ['-date']
    search_fields = ['description']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to edit this expense.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this expense.")
        instance.delete()

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        now = timezone.now()
        queryset = self.get_queryset().filter(
            date__year=now.year,
            date__month=now.month
        )
        aggregates = queryset.aggregate(
            total=Sum('amount'),
            expense_count=Count('id'),
            average=Avg('amount')
        )
        return Response({
            'month': now.strftime('%B %Y'),
            'total': aggregates['total'] or '0.00',
            'expense_count': aggregates['expense_count'] or 0,
            'average': round(aggregates['average'], 2) if aggregates['average'] else '0.00',
        })

    @action(detail=False, methods=['get'], url_path='by-category')
    def by_category(self, request):
        queryset = self.get_queryset()
        total_spent = queryset.aggregate(
            total=Sum('amount')
        )['total'] or 0
        categories = (
            Category.objects
            .filter(user=request.user)
            .annotate(
                total=Sum('expenses__amount'),
                expense_count=Count('expenses__id')
            )
            .filter(total__isnull=False)
            .order_by('-total')
        )
        data = []
        for cat in categories:
            percentage = (
                round((cat.total / total_spent) * 100, 1)
                if total_spent > 0 else 0
            )
            data.append({
                'category_id': cat.id,
                'category_name': cat.name,
                'color': cat.color,
                'icon': cat.icon,
                'total': cat.total,
                'expense_count': cat.expense_count,
                'percentage': percentage,
            })
        return Response(data)