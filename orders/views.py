from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from inventory.models import InventoryItem, Order
from .forms import OrderForm
from django.contrib import messages
from django.urls import reverse_lazy

# Create your views here.
class Index(TemplateView):
	template_name = 'orders/orders.html'

#Clase para listar todas las ordenes a Items creadas
class Orders(LoginRequiredMixin, ListView, FormView):
	model = Order
	form_class = OrderForm
	template_name = 'orders/orders.html'
	success_url = '/orders/'
	success_message = "Order has been created successfully"
		
	items = InventoryItem.objects.all()
	orders = Order.objects.all().order_by()

	def get(self, request):
		orders = Order.objects.all().order_by('-date', 'event')	
		return render(request, 'orders/orders.html', {'orders': orders, 'title': "Orders", 'form': self.get_form()})

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["items"] = self.items
		context["orders"] = self.orders
		context['form'] = self.get_form()
		context["title"] = 'Orders'
		return context
	
	def form_valid(self, form):
		form.instance.user = self.request.user
		order_quantity = form.cleaned_data['order_quantity']
		order_product = form.cleaned_data['product']
		order_event = form.cleaned_data['event']

		product = InventoryItem.objects.get(name=order_product)
		
		if product is not None and order_quantity > product.quantity:
			messages.warning(self.request, "La cantidad a ordenar no puede ser cubierta por el inventario")
			return self.form_invalid(form)

		product.quantity -= order_quantity
		product.save()
		form.save()
		return super().form_valid(form)
			
#Clase para editar ua orden
class EditOrder(LoginRequiredMixin, UpdateView):
	model = Order
	form_class = OrderForm
	template_name = 'orders/order_form.html'
	success_url = reverse_lazy('orders')
	success_message = "Order has been edited successfully"

	def get_context_data(self, **kwargs):                                               
		context = super().get_context_data(**kwargs)
		context["title"] = 'Edit Order'
		context["savebtn"] = 'Update Order'
		context["delbtn"] = 'Delete Order'
		return context

#Clase para eliminar una orden
class DeleteOrder(LoginRequiredMixin, DeleteView):
	model = Order
	template_name = 'orders/delete_order.html'
	success_url = reverse_lazy('orders')
	context_object_name = 'order'
	success_message = "Order has been deleted successfully"
	Items = InventoryItem.objects.all()

	def post(self, request, pk):
		order = self.get_object()
		order_id = pk
		print(order_id)
		
		product = get_object_or_404(self.Items, name=order.product)
		print(product)
		product.quantity += order.order_quantity
		product.save()
		return super().delete(self, request)
