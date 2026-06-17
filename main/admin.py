from django.contrib import admin
from .models import House, Ramps, Availability, Elevator, City

# Register your models here.
admin.site.register(City)
admin.site.register(House)
admin.site.register(Ramps)
admin.site.register(Availability)
admin.site.register(Elevator)
