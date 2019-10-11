from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.core.cache import cache
from ..models import Sale
from ..serializers import SaleSerializer
from ..tasks import print_sale_check, print_refund_check


class SaleView(viewsets.ModelViewSet):
    """"""

    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAdminUser]

    def create(self, request, *args, **kwargs):
        if cache.get('CASHIER_IS_OPEN', False):
            resp = super().create(request)
            print_sale_check.delay(resp.data)
            return resp
        #else:
        #    return Response({
        #        'error': 'Please open cash.',
        #    }, 412)

    #add if
    def perform_destroy(self, instance):
        instance.refund = True
        instance.save()
        print_refund_check.delay(self.serializer_class(instance).data)
