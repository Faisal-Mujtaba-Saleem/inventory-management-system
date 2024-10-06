from django.contrib import admin
from .models import Item, Stock, Category, SubCategory, Supplier, Supply

# Register your models here.

admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Supplier)
admin.site.register(Supply)
