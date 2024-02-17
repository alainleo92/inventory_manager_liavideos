from django import forms
from inventory.models import InventoryItem, Order


class OrderForm(forms.ModelForm):
	class Meta:
		model = Order
		fields = ['event', 'product', 'order_quantity']

	def __init__(self, *args, **kwargs):
		super(OrderForm, self).__init__(*args, **kwargs)
		# self.helper = FormHelper()
		# self.helper.layout = Layout(
		# 	Field('even', label="Nombre del evento", 

		# 	)
		# )

		self.fields['product'].queryset = InventoryItem.objects.filter(quantity__gt=0).order_by('name')
