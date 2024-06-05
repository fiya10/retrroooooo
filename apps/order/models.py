from django.db import models
from django.contrib.auth.models import User
from apps.store.models import Product

class Order(models.Model):
    STATUS_ORDERED = 'ordered'
    STATUS_SHIPPED = 'shipped'
    STATUS_ARRIVED = 'arrived'

    STATUS_OPTIONS = (
        (STATUS_ORDERED, 'Ordered'),
        (STATUS_SHIPPED, 'Shipped'),
        (STATUS_ARRIVED, 'Arrived')
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    payment_intent = models.CharField(max_length=255, blank=True, null=True)
    shipped_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_OPTIONS, default=STATUS_ORDERED)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'Order Item {self.id}'
