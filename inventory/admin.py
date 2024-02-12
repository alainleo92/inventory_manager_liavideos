from django.contrib import admin
from .models import InventoryItem, Category, Order, Evento

admin.site.register(InventoryItem)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Evento)

