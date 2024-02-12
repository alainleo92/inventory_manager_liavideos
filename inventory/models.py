from django.db import models
from django.contrib.auth.models import User
import uuid

# CATEGORY = (
#     ("Camaras", "Camaras"),
#     ("Informatica", "Informatica"),
#     ("Sonido", "Sonido"),
# )

class InventoryItem(models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name="Name")
	quantity = models.PositiveIntegerField(default=1)
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
	description = models.TextField()
	localitation = models.CharField(max_length=40, null=True)
	inv_ID = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name
	
class Evento(models.Model):
	name = models.CharField(max_length=200, unique=True, verbose_name="Name")
	description = models.CharField(max_length=1000, null=True)
	localitation = models.CharField(max_length=40, null=True)
	tech = models.CharField(max_length=50, null=True, default='Juan Perez')
	tech_CI = models.PositiveIntegerField(default='92121354653')
	date_created = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	# order = models.ForeignKey('Order', on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Order(models.Model):
	event = models.ForeignKey(Evento, on_delete=models.CASCADE)
	product = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	order_quantity = models.PositiveIntegerField(null=True, default=1)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"{self.product} ordered quantity {self.order_quantity} for {self.event}"