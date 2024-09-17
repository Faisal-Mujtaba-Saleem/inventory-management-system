from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name="Item Name", max_length=50)
    qty = models.IntegerField(verbose_name="Quantity", default=0)
    price = models.IntegerField(verbose_name="Price", default=0)
    description = models.TextField(
        verbose_name="Description", blank=True, max_length=1000
    )
    category = models.CharField(verbose_name="category", max_length=50)
