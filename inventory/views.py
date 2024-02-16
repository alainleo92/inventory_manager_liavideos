from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView, ListView, FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, OrderForm, EventoForm, forms
from .models import InventoryItem, Category, Order, Evento
from inventory_management.settings import LOW_QUANTITY
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Sum

class Index(TemplateView):
	template_name = 'inventory/login.html'

#Clase para registrar un nuevo usuario
class SignUpView(View):
	def get(self, request):
		form = UserRegisterForm()
		return render(request, 'inventory/signup.html', {'form': form})

	def post(self, request):
		form = UserRegisterForm(request.POST)

		if form.is_valid():
			form.save()
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1']
			)

			login(request, user)
			return redirect('index')

		return render(request, 'inventory/signup.html', {'form': form, 'title': "Signup"})

#Clase para ver un resumen de todo 
class Dashboard(LoginRequiredMixin, View):
	def get(self, request):
		users = User.objects.all()[:2]
		items = InventoryItem.objects.all()[:3]
		orders = Order.objects.all()[0:3]
		eventos = Evento.objects.all()[0:3]
		reg_user = len(User.objects.all())
		all_prods = len(InventoryItem.objects.all())
		all_orders = len(Order.objects.all())
		all_events = len(Evento.objects.all())

		context = {
        	"users": users,
        	"items": items,
			"orders": orders,
			"eventos": eventos,
        	"count_users": reg_user,
        	"count_products": all_prods,
			"count_orders": all_orders,
			"count_events": all_events,
			'title': "Dashboard" 
    	}
		return render(request, "inventory/dashboard.html", context)

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

#Clase para listar todas las ordenes a Items creadas
class Orders(LoginRequiredMixin, ListView, FormView):
	model = Order
	form_class = OrderForm
	template_name = 'inventory/orders.html'
	success_url = '/orders/'
	success_message = "Order has been created successfully"
		
	items = InventoryItem.objects.all()
	orders = Order.objects.all().order_by()

	def get(self, request):
		orders = Order.objects.all().order_by('-date', 'event')	
		return render(request, 'inventory/orders.html', {'orders': orders, 'title': "Orders", 'form': self.get_form()})

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
		
		
		# # order = Order.objects.get(product=order_product, event=order_event)
		
		# if Order.objects.get(product=order_product, event=order_event) is not None:
		# 	order = Order.objects.get(product=order_product, event=order_event)
		# 	order.order_quantity += order_quantity
		# 	order.save()
		# else:
		# 	form.save()
		# 	return super().form_valid(form)
			
#Clase para editar ua orden
class EditOrder(LoginRequiredMixin, UpdateView):
	model = Order
	form_class = OrderForm
	template_name = 'inventory/order_form.html'
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
	template_name = 'inventory/delete_order.html'
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

#Clase para visualizar todos los eventos creados
class Eventos(LoginRequiredMixin, ListView, FormView):
	model = Evento
	form_class = EventoForm
	template_name = 'inventory/events.html'
	success_url = '/events/'
	success_message = "Event has been created successfully"
	
	def get(self, request):
		eventos = Evento.objects.all().order_by('id')
		
		context = {
			'eventos': eventos,
			'title': "Eventos",
			'form': self.get_form()
			}
		return render(request, 'inventory/events.html', context)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = self.get_form()
		return context

	def form_valid(self, form):
		form.instance.user = self.request.user
		form.save()
		return super().form_valid(form)

#Clase para editar un evento
class EditEvento(LoginRequiredMixin, UpdateView):
	model = Evento
	form_class = EventoForm
	template_name = 'inventory/event_form.html'
	success_url = reverse_lazy('events')
	success_message = "Event has been edited successfully"

	def get_context_data(self, **kwargs):                                               
		context = super().get_context_data(**kwargs)
		context["title"] = 'Edit Event'
		context["savebtn"] = 'Update Event'
		context["delbtn"] = 'Delete Event'
		return context

#Clase para eliminar un evento
class DeleteEvento(LoginRequiredMixin, DeleteView):
	model = Evento
	template_name = 'inventory/delete_event.html'
	success_url = reverse_lazy('events')
	context_object_name = 'event'
	success_message = "Event has been deleted successfully"

	def post(self, request, pk):
		evento_id = pk
		
		orders = Order.objects.filter(event_id=evento_id)

		for order in orders:
			product = InventoryItem.objects.get(name=order.product)
			print(product)
			product.quantity += order.order_quantity
			product.save()
		return super().delete(self, request)

#Clase para ver las ordenes de un evento seleccionado
class Check_Evento(LoginRequiredMixin, ListView):
	def get(self, request, event_id):	
		check_orders = Order.objects.filter(event=event_id).values('product__name').annotate(total=Sum('order_quantity')).order_by('product__category', 'product__name')		
		
		agrupado = {}
		for product in check_orders:
			if product["product__name"] in agrupado:
				agrupado[product["product__name"]] += product["total"]
			else:
				agrupado[product["product__name"]] = product["total"]

		check_event = Evento.objects.get(id=event_id)
		orders = Order.objects.filter(event=event_id)

		all_orders = Order.objects.filter(event=event_id).values('product__name').aggregate(total=Sum('order_quantity'))
		all_orders = all_orders['total']
		
		context = {
			'orders': orders,
			'title': check_event.name,
			'all_orders': all_orders,
			'evento_id': check_event.id,
			'agrupado': agrupado,
			}
		return render(request, 'inventory/event.html', context)
