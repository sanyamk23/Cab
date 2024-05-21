from django.contrib import admin
from .models import Customer, Driver, RideRequest

class CustomerDisplay(admin.ModelAdmin):
    list_display = ('username', 'email')

admin.site.register(Customer,CustomerDisplay)
admin.site.register(Driver)
admin.site.register(RideRequest)