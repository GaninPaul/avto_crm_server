from rest_framework import viewsets, permissions
from ..serializers import ProductSerializers
from ..models import Product


class ProductView(viewsets.ModelViewSet):
    """Product end point"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
