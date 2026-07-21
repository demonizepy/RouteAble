from django.contrib import admin
from .models import House, Availability

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'number', 'has_elevator', 'has_ramp', 'user')
    list_filter = ('has_elevator', 'has_ramp', 'city')
    search_fields = ('city', 'street', 'number')

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'assistance')