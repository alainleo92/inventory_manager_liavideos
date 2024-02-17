from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from inventory.models import InventoryItem, Order, Evento
from .forms import EventoForm
from django.db.models import Sum

# Create your views here.
class Index(TemplateView):
	template_name = 'events/events.html'

#Clase para visualizar todos los eventos creados
class Eventos(LoginRequiredMixin, ListView, FormView):
	model = Evento
	form_class = EventoForm
	template_name = 'events/events.html'
	success_url = '/events/'
	success_message = "Event has been created successfully"
	
	def get(self, request):
		eventos = Evento.objects.all().order_by('id')
		
		context = {
			'eventos': eventos,
			'title': "Eventos",
			'form': self.get_form()
			}
		return render(request, 'events/events.html', context)

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
	template_name = 'events/event_form.html'
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
	template_name = 'events/delete_event.html'
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
		return render(request, 'events/event.html', context)

