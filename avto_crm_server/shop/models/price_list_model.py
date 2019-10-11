from django.db import models


class PriceListMixin(models.Model):

    product = models.ForeignKey('Product', verbose_name="Продукт", on_delete=models.PROTECT)
    date = models.DateTimeField("Дата установки цены", auto_now_add=True)
    price = models.FloatField("Цена")

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.product)


class RetailPriceList(PriceListMixin):

    class Meta:
        ordering = ['-date']
        verbose_name = "Розничная цена"
        verbose_name_plural = "Розничные цены"


class WholesalePriceList(PriceListMixin):

    class Meta:
        ordering = ['-date']
        verbose_name = "Оптовая цена"
        verbose_name_plural = "Оптовые цены"
