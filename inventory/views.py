from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, ListView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import InventoryItemForm
from .models import InventoryItem, Category
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.

#Clase para visualizar todos los productos del inventario y se emite una alerta sobre bajo inventario
class Items(LoginRequiredMixin, ListView, FormView):
	model = InventoryItem
	form_class = InventoryItemForm
	items = InventoryItem.objects.all().order_by('name')
	template_name = 'items/items.html'
	success_url = '/items/'
	success_message = "Stock has been created successfully"
	
	def get(self, request):
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
	
		consulta = self.items
		paginacion = Paginator(consulta,8)
		page_number = request.GET.get('page')
		consulta = paginacion.get_page(page_number)
		
		context = {
			'items': consulta, 
			'low_inventory_ids': low_inventory_ids,
			'title': "Items",
			'form': self.get_form(),
			'page_obj' : consulta,
			}

		query = self.request.GET.get('q')
		if query:
			context['items']=InventoryItem.objects.filter(name__icontains=query)
			context['page_obj']=InventoryItem.objects.filter(name__icontains=query)
			
		return render(request, 'items/items.html', context)

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return super().form_valid(form)
	
#Clase para modificar un Item
class EditItem(LoginRequiredMixin, UpdateView):
	model = InventoryItem
	form_class = InventoryItemForm
	template_name = 'items/item_form.html'
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
	template_name = 'items/delete_item.html'
	success_url = reverse_lazy('items')
	context_object_name = 'item'
	success_message = "Stock has been deleted successfully"

