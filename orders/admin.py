from django.contrib import admin
from .models import OrderItem , Order
from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.
import csv
import datetime
from django.http import HttpResponse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def export_csv(modeladmin , request, queryset):
    opts = modeladmin.model._meta
    content = 'attchment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = content
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj,field.name)
            if isinstance(value,datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_csv.short_description = "Export to CSV"


def order_detail(obj):
    url = reverse("orders:admin_order_detail",args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_pdf(obj):
    url = reverse("orders:admin_order_pdf",args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_pdf.short_description = "Export to pdf"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','paid',order_detail,order_pdf]
    list_filter = ('paid','created','update')
    inlines = [OrderItemInline]
    actions = [export_csv]
