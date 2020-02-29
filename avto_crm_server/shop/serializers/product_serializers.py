from rest_framework import serializers
from ..models import Product, Category, Tag


class ProductSerializers(serializers.HyperlinkedModelSerializer):
    """Product serializers class"""

    product_wholesale_price = serializers.FloatField(
        source='wholesale_price',
        label='Оптовая цена',
        required=False
    )
    product_retail_price = serializers.FloatField(
        source='retail_price',
        label='Розничная цена',
        required=False
    )
    product_tags = serializers.ListField(
        child=serializers.CharField(),
        source='tags',
        label='Лист тегов',
        required=False,
    )

    def create(self, validated_data):
        wholesale_price = validated_data.pop('wholesale_price')
        retail_price = validated_data.pop('retail_price')
        tags = validated_data.pop('tags', [])
        obj = super().create(validated_data)
        obj.wholesale_price = wholesale_price
        obj.retail_price = retail_price
        obj.tags = tags
        return obj

    class Meta:
        model = Product
        fields = (
            'id', 'url', 'name',
            #'category',
            'product_tags', 'description',
            'bar_code', 'amount',
            'product_wholesale_price', 'product_retail_price',
        )
