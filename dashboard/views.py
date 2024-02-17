from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from inventory.models import InventoryItem, Category, Order, Evento
from django.contrib.auth.models import User

# Create your views here.
class Index(TemplateView):
	template_name = 'dashboard/dash.html'

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
		return render(request, "dashboard/dash.html", context)