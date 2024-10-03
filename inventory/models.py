from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.


class Category(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(
        verbose_name="SubCategory Name",
        unique=True,
        max_length=50
    )
    slug = models.SlugField(
        verbose_name="SubCategory Slug",
        unique=True,
        editable=False,
        max_length=50,
    )
    category = models.ForeignKey(
        to=Category,
        verbose_name="category",
        on_delete=models.CASCADE
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Item(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
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
    price = models.PositiveIntegerField(
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
    sub_category = models.ForeignKey(
        to=SubCategory,
        verbose_name="sub_category",
        on_delete=models.CASCADE
    )
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    updatedAt = models.DateTimeField(
        verbose_name="updatedAt",
        auto_now=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.sku)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Stock(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    item = models.OneToOneField(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='Item'
    )
    qty_in_stock = models.PositiveIntegerField(default=0)
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.qty_in_stock} in stock"


class Supplier(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    name = models.CharField(verbose_name="Supplier Name", max_length=50)
    email = models.EmailField(
        verbose_name="Email",
        unique=True,
        max_length=100
    )
    phone = models.CharField(
        verbose_name="Phone Number",
        unique=True,
        max_length=15
    )
    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    updatedAt = models.DateTimeField(
        verbose_name="updatedAt",
        auto_now=True
    )

    def __str__(self):
        return self.name


class Supply(models.Model):
    id = models.AutoField(verbose_name="ID", primary_key=True)
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        verbose_name='Item'
    )
    supplier = models.ForeignKey(
        to=Supplier,
        verbose_name="Supplier",
        on_delete=models.CASCADE
    )
    qty_supplied = models.PositiveIntegerField(default=0)

    recordedAt = models.DateTimeField(
        verbose_name="recordedAt",
        auto_now_add=True
    )
    updatedAt = models.DateTimeField(
        verbose_name="updatedAt",
        auto_now=True
    )

    def save(self, *args, **kwargs):
        stock = Stock.objects.filter(item=self.item).first()
        if stock:
            if stock.qty_in_stock >= self.qty_supplied:
                stock.qty_in_stock -= self.qty_supplied
                stock.save()

                return super().save(*args, **kwargs)
            else:
                raise ValueError(
                    f"Insufficient stock for item {self.item.name}. Available: {
                        stock.qty_in_stock}, requested: {self.qty_supplied}"
                )
        else:
            raise Exception(f"Stock not found for item {self.item.name}")

    def __str__(self):
        return f"{self.item.name_of_item.name} - {self.qty_supplied} supplied"
