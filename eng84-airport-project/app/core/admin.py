from django.contrib import admin
from .models import Person, Staff, Passenger, Flight, Aircraft


admin.site.register(Passenger)
admin.site.register(Staff)
admin.site.register(Flight)
admin.site.register(Aircraft)
