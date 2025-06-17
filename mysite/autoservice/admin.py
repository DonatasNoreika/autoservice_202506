from django.contrib import admin
from .models import CarModel, Service, Car, Order, OrderLine

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date']
    inlines = [OrderLineInLine]

class CarAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'car_model', 'licence_plate', 'vin_number']
    list_filter = ['client_name', 'car_model']
    search_fields = ['licence_plate', 'vin_number', 'car_model__make', 'car_model__model']

class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

# Register your models here.
admin.site.register(CarModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)