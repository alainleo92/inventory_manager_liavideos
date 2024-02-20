from django.contrib import admin
from .models import InventoryItem, Category, Order, Evento

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category', 'description', 'localitation')
    list_filter = ('category',)


admin.site.register(InventoryItem, ItemAdmin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Evento)

