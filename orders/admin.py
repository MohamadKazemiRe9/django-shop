from django.contrib import admin
from .models import OrderItem , Order
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','address','postal_code','city','paid','created','update']
    list_filter = ('paid','created','update')
    inlines = [OrderItemInline]

