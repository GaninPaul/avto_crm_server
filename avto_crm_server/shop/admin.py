from django.contrib import admin
from .models import *


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'bar_code',
        'amount',
        'wholesale_price',
        'retail_price',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'position'
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(WholesalePriceList)
class WholesalePriceListAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'date',
        'price',
    )


@admin.register(RetailPriceList)
class RetailPriceListAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'date',
        'price',
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'purchase_type',
        'payment_method',
        'refund',
        'shopping_list',
    )

    def shopping_list(self, obj):
        return ", ".join(['{}-{}'.format(i.product.name, i.product.bar_code) for i in obj.shopping_list])


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    pass
