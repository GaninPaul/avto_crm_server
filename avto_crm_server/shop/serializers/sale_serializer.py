from rest_framework import serializers
from ..models import Sale, ShoppingListItem


class ShoppingListItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShoppingListItem
        fields = (
            'product',
            'count',
            'price'
        )


class SaleSerializer(serializers.ModelSerializer):

    product_list = ShoppingListItemSerializer(
        many=True,
        source='shopping_list',
    )

    class Meta:
        model = Sale
        fields = (
            'id',
            'purchase_type',
            'payment_method',
            'refund',
            'date',
            'product_list'
        )
        extra_kwargs = {
            'refund': {'read_only': True},
        }

    def create(self, validate_data):
        products = validate_data.pop('shopping_list')
        obj = super().create(validate_data)
        for product in products:
            ShoppingListItem.objects.create(sale=obj, **product)
        return obj
