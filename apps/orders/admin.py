import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from .models import Order, OrderItem


def ExportToCSV(modeladmin, request, queryset):
    _ = request
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    now = datetime.datetime.now().strftime('%d/%m/%Y')
    str_to_format = 'attachment; filename=Orders-{}.csv'
    response['Content-Disposition'] = str_to_format.format(now)
    writer = csv.writer(response)

    fields = []
    for field in opts.get_fields():
        if not field.many_to_many and not field.one_to_many:
            fields.append(field)

    # first string - header
    writer.writerow([field.verbose_name for field in fields])

    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


def order_detail(obj):
    return format_html('<a href="{}">Подивитися</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])
    ))


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'carrier', 'city',
                    'warehouse_num', 'phone_num', 'paid', 'created', 'updated',
                    order_detail]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [ExportToCSV]


admin.site.register(Order, OrderAdmin)
