from rest_framework import serializers
from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'icon']
        read_only_fields = ['id']

    def validate(self, data):
        request = self.context.get('request')
        name = data.get('name')
        instance = self.instance

        qs = Category.objects.filter(
            user=request.user,
            name=name
        )
        if instance:
            qs = qs.exclude(pk=instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                {'name': 'You already have a category with this name.'}
            )
        return data

class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source ='category.name',
        read_only=True
    )

    class Meta:
        model = Expense
        fields = [
            'id',
            'amount',
            'description',
            'date',
            'category',
            'category_name',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']