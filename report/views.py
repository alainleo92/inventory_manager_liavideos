from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from xhtml2pdf import pisa
from io import BytesIO
from inventory.models import InventoryItem, Order, Evento, Category
from inventory.views import Check_Evento
from django.db.models import Sum

# Create your views here.
class Export_Event(LoginRequiredMixin, View):
    def get(self, request, event_id):
        check_orders = Order.objects.filter(event=event_id).values('product__name').annotate(total=Sum('order_quantity')).order_by('product__name')
        
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
        
        #Enviar el contexto a la plantilla
        context = {
			'orders': orders,
			'title': check_event.name,
			'all_orders': all_orders,
			'evento_id': check_event.id,
			'agrupado': agrupado,
            'tech': check_event.tech,
            'tech_CI': check_event.tech_CI,
			}
        
        template = 'report/report-pdf.html'

        #Llamar a la funcion para generar el PDF y devolverlo
        pdf = self.render_to_pdf(template, context)
        return HttpResponse(pdf, content_type='application/pdf')
    
    def render_to_pdf(self, template_src, context_dict):
        # Obtén la plantilla HTML que deseas convertir en PDF
        template = get_template(template_src)
        html = template.render(context_dict)
       
        # Crea un archivo PDF en memoria
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

        # Si no hay errores, devuelve el archivo PDF como respuesta HTTP
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')

        # Si hay errores, devuelve una respuesta de error
        return HttpResponse('Error al generar el PDF: ')
        