from django.contrib import admin
from . models import *

admin.site.register(BusinessInfo)

class FlightAdmin(admin.ModelAdmin):
    list_display=('client_name', 'departure', 'destination', 'Round_trip')

admin.site.register(Flight_request, FlightAdmin)
admin.site.register(new_contact)
admin.site.register(Visa_Service_Countries)
admin.site.register(Package)
admin.site.register(deals_event)

