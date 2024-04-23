from django.contrib import admin
from . models import *

admin.site.register(BusinessInfo)

class FlightAdmin(admin.ModelAdmin):
    list_display=('client_name', 'departure', 'destination', 'Round_trip', 'Date')
    
class Inquiries(admin.ModelAdmin):
    list_display=('client_name', 'client_contact', 'client_subject')

admin.site.register(Flight_request, FlightAdmin)
admin.site.register(new_contact, Inquiries)
admin.site.register(Visa_Service_Countries)
admin.site.register(Package)
admin.site.register(deals_event)
admin.site.register(Itinerary)
admin.site.register(Highlight)
admin.site.register(Inclusion)
admin.site.register(Exclusion)
admin.site.register(Company_Members)

