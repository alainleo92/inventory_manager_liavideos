from collections.abc import Mapping
from typing import Any
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.postgres.search import TrigramSimilarity
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Order, InventoryItem, Evento
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class InventoryItemForm(forms.ModelForm):
	# category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
	class Meta:
		model = InventoryItem
		fields = ['name', 'quantity', 'category', 'localitation', 'description']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Field('name', label='Nombre del producto', css_class='form-group', id='name'),
			Field('quantity', label='Cantidad', css_class='form-group'),
			Field('category', label='Categoria', css_class='form-group'),
			Field('localitation', label='Localizacion del producto', css_class='form-group', row=3, widget=forms.Textarea)
		)