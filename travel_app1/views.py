import csv
from io import StringIO
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import requests
from travel_app1.models import *
from travel_main import settings
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
# def index(request):
#     populate_airports()
#     airport = Airport.objects.all()
#     location_depart = Departure.objects.all()
#     location_desti = Destination.objects.all()
#     return render(request, 'index.html', {'depart': location_depart, 'desti': location_desti, 'airport': airport})




def index(request):
    # populate_airports()
    info = BusinessInfo.objects.all().first()
    airport = Airport.objects.none()
    package = Package.objects.all()
    
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        airport = Airport.objects.filter(Q(name__icontains=search_query) | Q(location_name__icontains=search_query) | Q(country__icontains=search_query) | Q(iata_code__icontains=search_query))[:5]
        

    return render(request, 'index.html', {'airport': airport, 'info':info, 'package': package})

def main(request):
    
    info = BusinessInfo.objects.all().first()
    content = {'info':info}
    
    return render(request, 'mainLayout.html', content)


# def search_airports(request):
#     if 'search_query' in request.GET:
#         search_query = request.GET['search_query']
#         airports = Airport.objects.filter(Q(name__icontains=search_query) | Q(location_name__icontains=search_query) | Q(country__icontains=search_query) | Q(iata_code__icontains=search_query))[:10]  # Limit results to 5
#         data = [{'name': airport.name, 'location_name': airport.location_name, 'country': airport.country, 'iata_code' : airport.iata_code} for airport in airports]
#         return JsonResponse(data, safe=False)
#     return JsonResponse([], safe=False)


from django.db.models import Case, Value, When, CharField

def search_airports(request):
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        airports = Airport.objects.annotate(
            is_nepal=Case(
                When(country='NP', then=Value(1)),
                default=Value(0),
                output_field=CharField(),
            ),
            has_iata_code=Case(
                When(iata_code=search_query.upper(), then=Value(1)),
                default=Value(0),
                output_field=CharField(),
            )
        ).filter(
            Q(name__icontains=search_query) | 
            Q(location_name__icontains=search_query) | 
            Q(country__icontains=search_query) | 
            Q(iata_code__icontains=search_query)
        ).order_by('-is_nepal', '-has_iata_code')[:10]  # First show airports from Nepal, then those with matching IATA code
        data = [{'name': airport.name, 'location_name': airport.location_name, 'country': airport.country, 'iata_code' : airport.iata_code} for airport in airports]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)
    
    

def contact(request):
    info = BusinessInfo.objects.all().first()
    content = {'info':info}
    
    return render(request, 'contact.html', content)

def send_message(request):
    info = BusinessInfo.objects.all().first()
    if request.method == 'POST':
            name = request.POST.get('name')
            contact = request.POST.get('contact')
            subject = request.POST.get('subject')
            msg = request.POST.get('message')
        
            if name and contact and subject and msg:
                cnt = new_contact(client_name = name, client_contact = contact, client_subject= subject, client_message = msg)
                cnt.save()
                # messages.success(request, "Your message has been sent.")
        
                sub = "INQUIRY: " + subject
                message = "Client Name: " + name + " \n" + "Client Contact: " + contact + " \n" + "Subject: " + subject + " \n" + "Message: " + msg
                from_email = settings.EMAIL_HOST_USER
                to_list = [info.Business_Email]
                send_mail(sub, message, from_email, to_list, fail_silently=True)
        
                response_data = {'error' : False}
                
            else:
                response_data = {'error' : True}

    return JsonResponse(response_data)

def request_flight(request):
    info = BusinessInfo.objects.all().first()
    if request.method == 'POST':
        name = request.POST.get('cname')
        email = request.POST.get('cemail')
        contact = request.POST.get('cphone')
        depart_from = request.POST.get('cDeparture')
        desti_to = request.POST.get('cDestination')
        departure_date = request.POST.get('cDepartureDate')
        type = request.POST.get('roundtriptype')
        date_return = request.POST.get('cReturnDate')
        ot_adult = request.POST.get('adult-input')
        ot_child = request.POST.get('child-input')
        ot_infant = request.POST.get('infant-input')
        rt_adult = request.POST.get('adult-inputr')
        rt_child = request.POST.get('child-inputr')
        rt_infant = request.POST.get('infant-inputr')

        if name and email and contact and depart_from and desti_to and departure_date and type:
            if type == 'True':
                if date_return:
                    cnt = Flight_request(client_name = name, client_email = email, client_phone =contact, departure = depart_from, destination = desti_to, departure_date = departure_date, Round_trip = True, return_date = date_return, Adult = rt_adult, Children = rt_child, Infant = rt_infant)
                    cnt.save()

                    sub = "New Flight Booking Requested"
                    message = "Client Name: " + name + " \n" + "Client Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'Round Trip' + " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "Return date: " + date_return + " \n" + "Adult: " + rt_adult + " \n" + "Children: " + rt_child + " \n" + "Infant: " + rt_infant
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [info.Business_Email]
                    send_mail(sub, message, from_email, to_list, fail_silently=True)

                    # sub = "Check your flight details for booking"
                    # message = "Full Name: " + name + " \n" + "Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'Round Trip' + " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "Return date: " + date_return + " \n" + " \n" + "We will contact you shortly."
                    # to_list = [email]
                    # send_mail(sub, message, from_email, to_list, fail_silently=True)
                    response_data = {'error2' : False}
                else:
                    response_data = {'error2' : True}
            else:
                # if name and email and contact and depart_from and desti_to and departure_date:
                    cnt = Flight_request(client_name = name, client_email = email, client_phone =contact, departure = depart_from, destination = desti_to, departure_date = departure_date, Adult = ot_adult, Children = ot_child, Infant = ot_infant)
                    cnt.save()

                    sub = "New Flight Booking Requested"
                    message = "Client Name: " + name + " \n" + "Client Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'One Trip'+ " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "Adult: " + ot_adult + " \n" + "Children: " + ot_child + " \n" + "Infant: " + ot_infant
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [info.Business_Email]
                    send_mail(sub, message, from_email, to_list, fail_silently=True)

                    # sub = "Check your flight details for booking"
                    # message = "Full Name: " + name + " \n" + "Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'One Trip' + " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "\n" + "We will contact you shortly."
                    # to_list = [email]
                    # send_mail(sub, message, from_email, to_list, fail_silently=True)

                    response_data = {'error' : False}
                # else:
                #     response_data = {'error' : True}
        else:
            response_data = {'error': True, 'error2': True}
    
    return JsonResponse(response_data)




def policy(request):
    info = BusinessInfo.objects.all().first()
    content = {'info':info}
    
    return render(request,'TermsConditions.html', content)

def about(request):
    info = BusinessInfo.objects.all().first()
    content = {'info':info}
    return render(request,'about.html', content)



def populate_airports():
    url = 'https://ourairports.com/data/airports.csv'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.text
        csv_file = StringIO(data)
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row['name']
            location_name = row['municipality']  # Assuming 'municipality' field contains the location name
            country = row['iso_country']  # Field for country code
            iata_code = row['iata_code'] if 'iata_code' in row else None  # Field for IATA code
            latitude = float(row['latitude_deg'])
            longitude = float(row['longitude_deg'])
            Airport.objects.create(name=name, location_name=location_name, country=country, iata_code=iata_code, latitude=latitude, longitude=longitude)
        print("All airports populated successfully.")
    else:
        print("Failed to retrieve data from OurAirports API")
        
        
def visaService(request):
    info = BusinessInfo.objects.all().first()
    vdata = Visa_Service_Countries.objects.all()
    content = {'info':info, 'vdata': vdata}
    return render(request, 'visa.html', content)


def package_detail(request, slug):
    info = BusinessInfo.objects.all().first()
    package = Package.objects.get(slug=slug)
    content = {'info':info, 'package': package}
    return render(request, 'Package_detail.html', content)