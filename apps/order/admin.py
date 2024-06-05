import datetime
from django.urls import reverse
from django.contrib import admin
from .models import Order, OrderItem

def get_full_name(obj):
    return '%s %s' % (obj.first_name, obj.last_name)
get_full_name.short_description = 'Full Name'

def mark_orders_as_shipped(modeladmin, request, queryset):
    for order in queryset:
        order.shipped_date = datetime.datetime.now()
        order.status = Order.SHIPPED
        order.save()
mark_orders_as_shipped.short_description = 'Mark as shipped'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', get_full_name, 'status', 'email', 'address', 'zipcode', 'place', 'phone', 'paid', 'paid_amount', 'payment_intent', 'created_at')
    list_filter = ('paid', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'address', 'zipcode', 'place', 'phone')
    inlines = [OrderItemInline]
    actions = [mark_orders_as_shipped]
    readonly_fields = ('paid_amount', 'created_at', 'payment_intent')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
