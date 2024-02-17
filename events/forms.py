from django import forms
from inventory.models import Evento

class EventoForm(forms.ModelForm):
	class Meta:
		model = Evento
		fields = ['name', 'description', 'localitation', 'tech', 'tech_CI']
