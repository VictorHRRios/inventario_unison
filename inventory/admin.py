from django.contrib import admin
from .models import Item, Report, Order, ShoppingCart

admin.site.register(Item)
admin.site.register(Report)
admin.site.register(Order)
admin.site.register(ShoppingCart)


# Register your models here.
