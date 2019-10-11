from django.urls import path
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'products', ProductView)
router.register(r'sales', SaleView)

urlpatterns = [
    path(r'statistics/wholesale_price/product/<int:pk>', get_wholesale_price_list),
    path(r'statistics/retail_price/product/<int:pk>', get_retail_price_list),
    path(r'cashier/open', open_cashier_view),
    path(r'cashier/close', close_cashier_view),
    path(r'cashier/check', check_cashier_view),
]

urlpatterns += router.urls
