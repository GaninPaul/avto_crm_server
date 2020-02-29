from django.db import models
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from .price_list_model import WholesalePriceList, RetailPriceList


class Category(models.Model):

    name = models.CharField("Наименование", max_length=50, unique=True)
    position = models.IntegerField("Позиция")

    class Meta:
        ordering = ["position"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField("Наименование", max_length=50, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product model"""
    
    name = models.CharField("Наименование", max_length=50)
    category = models.ManyToManyField(Category, verbose_name="Категория", blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="Тег", blank=True)
    description = models.TextField("Описание")
    bar_code = models.IntegerField("Бар код")
    amount = models.IntegerField("Количество в упаковке")
    # photo

    wholesale_price = property(
        fget=lambda self: self._get_price(WholesalePriceList),
        fset=lambda self, val: self._set_price(WholesalePriceList, val)
    )
    retail_price = property(
        fget=lambda self: self._get_price(RetailPriceList),
        fset=lambda self, val: self._set_price(RetailPriceList, val)
    )
    #categorys = property()
    tags = property(
        fget=lambda self: [t for t in self.tag.all()],
        fset=lambda self, val: self._add_objects(Tag, val)
    )

    def _get_price(self, price_model):
        price_list = price_model.objects.filter(product_id=self.pk)
        max_date = price_list.aggregate(Max('date'))['date__max']
        return price_list.get(date=max_date).price

    def _set_price(self, price_model, value):
        price_model(product_id=self.pk, price=value).save()

    def _add_objects(self, field_type, value):
        for name in value:
            t, create = field_type.objects.get_or_create(name=name)
            self.tag.add(t)

    wholesale_price.fget.short_description = "Оптовая цена"
    retail_price.fget.short_description = "Розничная цена"
    tags.fget.short_description = "Тэг"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
