from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InventoryItemForm, forms
from .models import InventoryItem, Category, Order, Evento
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import JsonResponse

#Clase para visualizar todos los productos del inventario y se emite una alerta sobre bajo inventario
class Items(LoginRequiredMixin, ListView, FormView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/items.html'
	success_url = '/items/'
	success_message = "Stock has been created successfully"
	
	def get(self, request):
		items = InventoryItem.objects.all().order_by('name')
		
		low_inventory = InventoryItem.objects.filter(
			quantity__lte=LOW_QUANTITY
		)

		if low_inventory.count() > 0:
			if low_inventory.count() > 1:
				messages.error(request, f'{low_inventory.count()} artículos tienen un inventario bajo.')
			else:
				messages.error(request, f'{low_inventory.count()} artículo tiene un inventario bajo')

		low_inventory_ids = InventoryItem.objects.filter(
			quantity__lte=LOW_QUANTITY
		).values_list('id', flat=True)

		context = {
			'items': items, 
			'low_inventory_ids': low_inventory_ids,
			'title': "Items",
			'form': self.get_form(),
			}

		return render(request, 'inventory/items.html', context)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = Category.objects.all()
		context["title"] = 'New Item'
		context['form'] = self.get_form()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return super().form_valid(form)

#Clase para modificar un Item
class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'inventory/item_form.html'
	success_url = reverse_lazy('items')
	success_message = "Item has been modified successfully"

	def get_context_data(self, **kwargs):                                               
		context = super().get_context_data(**kwargs)
		context["title"] = 'Edit Item'
		context["savebtn"] = 'Update Item'
		context["delbtn"] = 'Delete Item'
		return context
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

#Clase para eliminar un Item
class DeleteItem(LoginRequiredMixin, DeleteView):
	model = InventoryItem
	template_name = 'inventory/delete_item.html'
	success_url = reverse_lazy('items')
	context_object_name = 'item'
	success_message = "Stock has been deleted successfully"
