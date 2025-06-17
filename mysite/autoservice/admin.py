from django.contrib import admin
from .models import CarModel, Service, Car, Order, OrderLine

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0
    fields = ['service', 'service_price_display', 'qty', 'line_sum']
    readonly_fields = ['line_sum', 'service_price_display']

    def service_price_display(self, obj):
        return obj.service.price
    service_price_display.short_description = 'Service Price'

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'total']
    inlines = [OrderLineInLine]

class CarAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'car_model', 'licence_plate', 'vin_number']
    list_filter = ['client_name', 'car_model']
    search_fields = ['licence_plate', 'vin_number', 'car_model__make', 'car_model__model']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['service', 'service__price', 'qty', 'line_sum']

# Register your models here.
admin.site.register(CarModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)