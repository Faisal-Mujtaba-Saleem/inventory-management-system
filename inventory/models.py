# from django.db import models

# # Create your models here.


# class Item(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(verbose_name="Item Name", max_length=50)
#     qty = models.IntegerField(verbose_name="Quantity", default=0)
#     price = models.IntegerField(verbose_name="Price", default=0)
#     description = models.TextField(
#         verbose_name="Description", blank=True, max_length=1000
#     )
#     category = models.CharField(verbose_name="category", max_length=50)

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Category Name",
        unique=True,
        max_length=50,
    )
    slug = models.SlugField(
        verbose_name="Category Slug",
        unique=True,
        editable=False,
        max_length=50,
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        verbose_name="Item Name",
        max_length=50
    )
    sku = models.CharField(
        verbose_name="SKU",
        unique=True, max_length=50
    )
    slug = models.SlugField(
        verbose_name="Item Slug",
        unique=True,
        editable=False,
        max_length=50,
    )
    price = models.IntegerField(
        verbose_name="Price",
        default=0
    )
    description = models.TextField(
        verbose_name="Description",
        max_length=1000
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name="category",
        on_delete=models.CASCADE
    )
    sub_category = models.CharField(
        verbose_name="sub_category",
        max_length=50,

    )
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    updatedAt = models.DateTimeField(verbose_name="updatedAt", auto_now=True)

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.OneToOneField(
        to='Item',
        on_delete=models.CASCADE,
        verbose_name='Item'
    )
    name = models.CharField(
        verbose_name="Name",
        max_length=50
    )
    sku = models.CharField(
        verbose_name="SKU",
        unique=True, max_length=50
    )
    slug = models.SlugField(
        verbose_name="Stock Slug",
        unique=True,
        editable=False,
        max_length=50,
    )
    qty_in_stock = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.qty_in_stock} in stock"


@receiver(signal=post_delete, sender=Item)
def delete_category_if_no_items_left(sender, instance, **kwargs):
    category = instance.category

    if not category.item_set.exists():
        category.delete()

