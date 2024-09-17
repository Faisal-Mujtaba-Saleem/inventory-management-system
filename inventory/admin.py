from django.contrib import admin
from .models import Item, Stock, Category

# Register your models here.

admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(Category)
