from rest_framework import serializers
from ..models import WholesalePriceList, RetailPriceList


class WholesalePriceListSerializers(serializers.ModelSerializer):
    """Wholesale price list serializers class"""

    class Meta:
        model = WholesalePriceList
        fields = (
            'price',
            'date',
        )


class RetailPriceListSerializers(serializers.ModelSerializer):
    """Retail price list serializers class"""

    class Meta:
        model = RetailPriceList
        fields = (
            'price',
            'date',
        )
