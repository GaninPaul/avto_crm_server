from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.core.cache import cache
from ..tasks import open_cashier, close_cashier


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def open_cashier_view(request):
    if not cache.get('CASHIER_IS_OPEN', False):
        cache.set('CASHIER_IS_OPEN', True)
        open_cashier.delay()
        return Response({'cashier': 'open'})
    else:
        return Response({'error': 'cashier already open'}, 412)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def close_cashier_view(request):
    if cache.get('CASHIER_IS_OPEN', False):
        cache.set('CASHIER_IS_OPEN', False)
        close_cashier.delay()
        return Response({'cashier': 'close'})
    else:
        return Response({'error': 'cashier is not open'}, 412)


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def check_cashier_view(request):
    if cache.get('CASHIER_IS_OPEN', False):
        return Response({'cashier': 'open'})
    else:
        return Response({'cashier': 'close'})
