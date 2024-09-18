from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Item Name",
        max_length=50
    )
    sku = models.CharField(verbose_name="SKU", unique=True, max_length=50)
    price = models.IntegerField(verbose_name="Price", default=0)
    description = models.TextField(
        verbose_name="Description",
        max_length=1000
    )
    category = models.CharField(
        verbose_name="category",
        max_length=50,

    )
    sub_category = models.CharField(
        verbose_name="sub_category",
        max_length=50,

    )
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.OneToOneField(
        to='Item',
        on_delete=models.CASCADE,
        verbose_name='Item'
    )
    name = models.CharField(verbose_name="Name", max_length=50)
    sku = models.CharField(verbose_name="SKU", max_length=50)
    qty_in_stock = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.qty_in_stock} in stock"


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name
