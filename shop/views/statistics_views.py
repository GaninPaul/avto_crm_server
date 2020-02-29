from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from ..models import WholesalePriceList, RetailPriceList
from ..serializers import WholesalePriceListSerializers, RetailPriceListSerializers


@api_view(['GET'])
def get_wholesale_price_list(request, pk):
    return Response({
        'product': pk,
        'price_list': _get_price_list(WholesalePriceList, WholesalePriceListSerializers, pk)
    })


@api_view(['GET'])
def get_retail_price_list(request, pk):
    return Response({
        'product': pk,
        'price_list': _get_price_list(RetailPriceList, RetailPriceListSerializers, pk)
    })


def _get_price_list(price_model, price_serializer, pk):
    product_price_list = get_list_or_404(price_model, product_id=pk)
    serializer = price_serializer(product_price_list, many=True)
    return serializer.data
