from django.db import models
from .product_model import Product


class Sale(models.Model):

    PAYMENT_METHOD = (
        ("cash", "Наличный расчет"),
        ("card", "Расчет картой")
    )

    PURCHASE_TYPE = (
        ("retail", "Розничная"),
        ("wholesale", "Оптовая"),
        ("custom", "Кастомная")
    )

    date = models.DateTimeField("Время продажи", auto_now_add=True)
    purchase_type = models.CharField(
        "Метод продажи",
        max_length=50,
        choices=PURCHASE_TYPE
    )
    payment_method = models.CharField(
        "Метод олаты",
        max_length=50,
        choices=PAYMENT_METHOD,
    )
    refund = models.BooleanField(
        "Возврат средств",
        default=False,
        null=True,
        blank=True
    )

    shopping_list = property(
        fget=lambda self: ShoppingListItem.objects.filter(sale_id=self.pk),
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "Продажа"
        verbose_name_plural = "Продажи"


class ShoppingListItem(models.Model):
    """"""

    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.PROTECT)
    count = models.IntegerField("Количество")
    price = models.FloatField("Цена")
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Элемент списка продаж"
        verbose_name_plural = "Элементы списка продаж"
