import csv
from datetime import timedelta
from io import StringIO
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
import requests
from travel_app1.models import *
from travel_main import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
from django.db.models import Case, Value, When, CharField
from django.shortcuts import render, redirect
from django.contrib import messages
import qrcode
from django.urls import reverse
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.shortcuts import render

def index(request):
    # populate_airports()
    info = BusinessInfo.objects.all().first()
    deal = deals_event.objects.all()
    airport = Airport.objects.none()
    package = Package.objects.filter(is_featured=True)
    
    if 'search_query' in request.GET:
        search_query = request.GET['search_query']
        airport = Airport.objects.filter(Q(name__icontains=search_query) | Q(location_name__icontains=search_query) | Q(country__icontains=search_query) | Q(iata_code__icontains=search_query))[:5]
        
    return render(request, 'index.html', {'airport': airport, 'info':info, 'package': package, 'deal': deal})

def main(request):
    
    info = BusinessInfo.objects.all().first()
    content = {'info':info}
    
    return render(request, 'mainLayout.html', content)


def admin_main(request):
    
    return render(request, 'AdminPanel/mainLayout.html',)


# def search_airports(request):
#     if 'search_query' in request.GET:
#         search_query = request.GET['search_query']
#         airports = Airport.objects.filter(Q(name__icontains=search_query) | Q(location_name__icontains=search_query) | Q(country__icontains=search_query) | Q(iata_code__icontains=search_query))[:10]  # Limit results to 5
#         data = [{'name': airport.name, 'location_name': airport.location_name, 'country': airport.country, 'iata_code' : airport.iata_code} for airport in airports]
#         return JsonResponse(data, safe=False)
#     return JsonResponse([], safe=False)


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
        ).order_by('-is_nepal', '-has_iata_code', '-iata_code')[:10]  # First show airports from Nepal, then those with matching IATA code
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
        input_onetrip = request.POST.get('traveler-input')
        input_rtrip = request.POST.get('traveler-inputr')

        if name and email and contact and depart_from and desti_to and departure_date and type:
            if type == 'True':
                if date_return:
                    if rt_adult or rt_child or rt_infant:
                        cnt = Flight_request(client_name = name, client_email = email, client_phone =contact, departure = depart_from, destination = desti_to, departure_date = departure_date, Round_trip = True, return_date = date_return, Adult = rt_adult, Children = rt_child, Infant = rt_infant)
                        cnt.save()

                        sub = "New Flight Booking Requested"
                        message = "Client Name: " + name + " \n" + "Client Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'Round Trip' + " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "Return date: " + date_return + " \n" + "Adult: " + rt_adult + " \n" + "Children: " + rt_child + " \n" + "Infant: " + rt_infant
                        from_email = settings.EMAIL_HOST_USER
                        to_list = [info.Business_Email]
                        send_mail(sub, message, from_email, to_list, fail_silently=True)

                        response_data = {'error2' : False}
                    else:
                        response_data = {'error2' : True}
                else:
                    response_data = {'error2' : True}
            else:
                if ot_adult or ot_child or ot_infant:
                    cnt = Flight_request(client_name = name, client_email = email, client_phone =contact, departure = depart_from, destination = desti_to, departure_date = departure_date, Adult = ot_adult, Children = ot_child, Infant = ot_infant)
                    cnt.save()

                    sub = "New Flight Booking Requested"
                    message = "Client Name: " + name + " \n" + "Client Email: " + email + " \n" + "Contact: " + contact + " \n" + "Trip Type: " + 'One Trip'+ " \n" + "Departure: " + depart_from + " \n" + "Destination: " + desti_to + " \n" + "Departure date: " + departure_date + " \n" + "Adult: " + ot_adult + " \n" + "Children: " + ot_child + " \n" + "Infant: " + ot_infant
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [info.Business_Email]
                    send_mail(sub, message, from_email, to_list, fail_silently=True)

                    

                    response_data = {'error' : False}
                else:
                    response_data = {'error' : True}
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
    info = BusinessInfo.objects.first()  
    itinerary = Itinerary.objects.filter(package__slug=slug)
    highlight = Highlight.objects.filter(package__slug=slug)
    inclusion = Inclusion.objects.filter(package__slug=slug)
    exclusion = Exclusion.objects.filter(package__slug=slug) 
    package = Package.objects.get(slug=slug)
    packages = Package.objects.exclude(slug=slug)[:3]
    

    return render(request, 'Package_detail.html', locals())

def packages(request):
    info = BusinessInfo.objects.all().first()
    package = Package.objects.all()
    content = {'info':info, 'package': package}
    return render(request, 'packages.html', content)


def staff(request, slug):
    try:
        info = BusinessInfo.objects.all().first()
        member = get_object_or_404(Company_Members, slug=slug)
        content = {'info': info, 'member': member}
        return render(request, 'Staff.html', content)
    except BusinessInfo.DoesNotExist:
        return HttpResponseNotFound("Business information not found")
    except Company_Members.DoesNotExist:
        return HttpResponseNotFound("Company member not found")
    except Exception as e:
        return HttpResponseServerError("Internal Server Error: " + str(e))



#Admin panel

@csrf_protect
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                if user.is_admin or user.is_member:
                    login(request, user)
                    print("User logged in successfully as admin")
                    return redirect('admin_flightrequest')
                else:
                    print("User is not an admin")
                    return render(request, 'AdminPanel/Login.html', {'error': 'Invalid user!'})
            else:
                print("User is inactive")
                return render(request, 'AdminPanel/Login.html', {'error': 'User account is inactive!'})
        else:
            print("Authentication failed")
            return render(request, 'AdminPanel/Login.html', {'error': 'Username or Password incorrect!'})

    return render(request, "AdminPanel/Login.html")


@csrf_protect
@login_required(login_url="admin_login")
def admin_signout(request):
    logout(request)
    return redirect('admin_login')


@csrf_protect
@login_required(login_url="admin_login")
def admin_visa(request):
    vdata = Visa_Service_Countries.objects.all()
    content = {'visa': vdata}
    return render(request, 'AdminPanel/visa.html', content)

@csrf_protect
@login_required(login_url="admin_login")
def search_visa_country(request):
    if request.method == "POST":
        query = request.POST.get("country-query")
        cn = Visa_Service_Countries.objects.filter(country_name__icontains=query)
    
        return render(request, "AdminPanel/visa.html", locals())

@csrf_protect
@login_required(login_url="admin_login")
def admin_addcountry(request):
    if request.method == 'POST':
        country_name = request.POST.get('name')  
        country_flag = request.FILES.get('flag') 

        country = Visa_Service_Countries(country_name=country_name, country_flag=country_flag)
        country.save()

        return redirect('admin_visa_service') 
    return render(request, "AdminPanel/addCountry.html", locals())


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewCountry(request, pk):
    try:
        country = Visa_Service_Countries.objects.get(pk=pk)
    except Visa_Service_Countries.DoesNotExist:
        return HttpResponseServerError("Country does not exist")

    if request.method == "POST":
        try:
            if 'name' in request.POST:
                country.country_name = request.POST['name']
            if 'flag' in request.FILES:
                country.country_flag = request.FILES['flag']

            country.save()

            return redirect('admin_visa_service')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"ctg": country}

    return render(request, "AdminPanel/viewCountry.html", context)



# QUOTATION - START

@csrf_protect
@login_required(login_url="admin_login")
def search_q(request):

    if request.method == "POST":
        query = request.POST.get("query")

        try:
            query_int = int(query)
            qu = quotation.objects.filter(Q(id__icontains=query_int) | Q(client_name__icontains=query) | Q(client_phone__icontains=query))
        except ValueError:
            qu = quotation.objects.filter(Q(client_name__icontains=query) | Q(client_phone__icontains=query))
    
        return render(request, "AdminPanel/quotation/Quotation.html", locals())
        

@login_required(login_url="admin_login")
def main_quotation(request):
    q = quotation.objects.all().order_by('-Date')
    return render(request, "AdminPanel/quotation/Quotation.html", locals())



@login_required(login_url="admin_login")
def add_quotation(request):
    try:
        if request.method == 'POST':
            cName = request.POST.get('cName')
            cPhone = request.POST.get('cPhone')
            cEmail = request.POST.get('cEmail')
            cPackage = request.POST.get('cPackage')
            perAdult = request.POST.get('perAdult')
            perChild = request.POST.get('perChild')
            perInfant = request.POST.get('perInfant')
            numAdult = request.POST.get('numAdult')
            numChild = request.POST.get('numChild')
            numInfant = request.POST.get('numInfant')

            int_adult, int_child, int_infant, num_adult, num_child, num_infant = 0,0,0,0,0,0

            if perAdult and perAdult.isdigit():
                int_adult = int(perAdult)
            

            if perChild and perChild.isdigit():
                int_child = int(perChild)

            if perInfant and perInfant.isdigit():
                int_infant = int(perInfant)

            
            if numAdult and numAdult.isdigit():
                num_adult = int(numAdult)
            

            if numChild and numChild.isdigit():
                num_child = int(numChild)

            if numInfant and numInfant.isdigit():
                num_infant = int(numInfant)

            

            receipt = quotation(
                client_name = cName,
                client_phone = cPhone,
                client_email = cEmail,
                package_name = cPackage,
                per_adult = int_adult,
                per_child = int_child,
                per_infant = int_infant,
                num_adult = num_adult,
                num_child = num_child,
                num_infant = num_infant,
            )

            receipt.save()
            return redirect('admin_quotation')

        return render(request, "AdminPanel/quotation/addQuotation.html", locals())
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message, status=500)


# Edit quotation
@csrf_protect
@login_required(login_url="admin_login")
def editquotation(request, q_id):
    quotations = quotation.objects.get(q_id=q_id)
    if request.method == 'POST':
        c_name = request.POST.get('c_name')
        c_phone = request.POST.get('c_phone')
        c_email = request.POST.get('c_email')
        package = request.POST.get('q_package')
        number_a = request.POST.get('q_num_adult')
        price_a = request.POST.get('q_per_adult')
        number_c = request.POST.get('q_num_child')
        price_c = request.POST.get('q_per_child')
        number_i = request.POST.get('q_num_infant')
        price_i = request.POST.get('q_per_infant')
        date = request.POST.get('q_date')


        quotations.client_name = c_name
        quotations.client_phone = c_phone
        quotations.client_email = c_email
        quotations.package_name = package
        quotations.num_adult = number_a
        quotations.per_adult = price_a
        quotations.num_child = number_c
        quotations.per_child = price_c
        quotations.num_infant = number_i
        quotations.per_infant = price_i
        quotations.q_Date = date

        quotations.save()

        return redirect('admin_viewQuotation', q_id)


# Quotation HTML view
@login_required(login_url="admin_login")
def admin_viewQuotation(request, q_id):
    invoice = quotation.objects.filter(q_id=q_id)
    ity = quotation_itinerary.objects.filter(q_id=q_id)
    inclu = quotation_inclusion.objects.filter(q_id=q_id)
    hotel = quotation_hotels.objects.filter(q_id=q_id)
    airline = quotation_airlines.objects.filter(q_id=q_id)



    content = {'id': q_id, 'invoices' : invoice, 'itys' : ity, 'inc': inclu, 'ht': hotel, 'air' : airline}

    return render(request, "AdminPanel/quotation/viewQuotation.html", content)


# For deleting Quotation
@login_required(login_url="admin_login")
def delete_adminquotation(request, pk):
    quo = get_object_or_404(quotation, pk=pk)
    quo.delete()
    return redirect(reverse("admin_quotation"))


# For itinerary
@login_required(login_url="admin_login")
def q_addItinerary(request, q_id):
    
    if request.method == 'POST':
        id = q_id
        date = request.POST.get('it-date')
        day = request.POST.get('it-day')
        ity = request.POST.get('itys')
        meal = request.POST.get('it-meal')

        Itinerarys = quotation_itinerary(q_id=id, date=date, day=day, Itinerary=ity, Meals=meal)
        Itinerarys.save()

        return redirect('admin_viewQuotation', q_id)

    all_ity = quotation_itinerary.objects.filter(q_id=q_id)
    new_date = None
    new_day = 0
    if all_ity:
        latest_ity = all_ity.order_by('-id')[0]

    # Get the date from the latest itinerary
        latest_date = latest_ity.date
        latest_day = latest_ity.day
        # Add one day to the latest date
        new_date = latest_date + timedelta(days=1)
        new_day = int(latest_day) + 1

    content = {'id': q_id, 'new_date' : new_date, 'new_day' : new_day}
    return render(request, "AdminPanel/quotation/addQuotation_itinerary.html", content)

@login_required(login_url="admin_login")
def search_meal(request):
    if 'ml_search_query' in request.GET:
        search_query = request.GET['ml_search_query']
        meals = quotation_fill_Meals.objects.filter(
            meals__icontains=search_query
        )[:10]
        data = [{'ml': meal.meals} for meal in meals]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

@login_required(login_url="admin_login")
def search_it(request):
    if 'it_search_query' in request.GET:
        search_query = request.GET['it_search_query']
        its = quotation_fill_Itinerary.objects.filter(
            itinerary__icontains=search_query
        )[:10]
        data = [{'ity': it.itinerary} for it in its]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)

# For viewing existing itinerary
@csrf_protect
@login_required(login_url="admin_login")
def admin_viewQuotationItinerary(request, itinerary_id):

    try:
        ity = quotation_itinerary.objects.get(id = itinerary_id)
    except quotation_itinerary.DoesNotExist:
        return HttpResponseServerError("Selected Highlight does not exist")

    if request.method == "POST":
        try:
            if 'it-date' in request.POST:
                ity.date = request.POST['it-date']

            if 'it-day' in request.POST:
                ity.day = request.POST['it-day']

            if 'itys' in request.POST:
                ity.Itinerary = request.POST['itys']

            if 'it-meal' in request.POST:
                ity.Meals = request.POST['it-meal']


            ity.save()

            return redirect('admin_viewQuotation', ity.q_id)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))
    print(ity.date)
    context = {"ity": ity, 'id': itinerary_id}

    return render(request, "AdminPanel/quotation/viewQuotationItinerary.html", context = context)

# for editing existing itinerary
@csrf_protect
@login_required(login_url="admin_login")
def quotation_editItenerary(request, itinerary_id):
    q_ity = quotation_itinerary.objects.get(id=itinerary_id)
    if request.method == 'POST':    
        date = request.POST.get('it-date')
        day = request.POST.get('it-day')
        ity = request.POST.get('itys')
        meal = request.POST.get('it-meal')
        q_ity.date = date
        q_ity.day = day
        q_ity.Itinerary = ity
        q_ity.Meals = meal
        q_ity.save()
        return redirect('admin_viewQuotation', q_ity.q_id)

    context = {'id': itinerary_id }
    return render(request, "AdminPanel/quotation/viewQuotationItinerary.html", context)

# for deleting itinerary object
@login_required(login_url="admin_login")
def delete_quotationItinerary(request, ity_id):
    itinerary = get_object_or_404(quotation_itinerary, pk=ity_id)
    itinerary.delete()
    return redirect('admin_viewQuotation', itinerary.q_id) 


# for inclusion
@login_required(login_url="admin_login")
def q_addinclusion(request, q_id):
    if request.method == 'POST':
        id = q_id
        inc = request.POST.get('inclun')
        exc = request.POST.get('exclu')

        InEx = quotation_inclusion(q_id=id, inclu=inc, exclu=exc)
        InEx.save()

        return redirect('admin_viewQuotation', q_id)
    
    content = {'id': q_id}
    return render(request, 'AdminPanel/quotation/addQuotation_inclusion.html', content)




@login_required(login_url="admin_login")
def search_in(request):
    if 'in_search_query' in request.GET:
        search_query = request.GET['in_search_query']
        inclus = quotation_fill_Inclusion.objects.filter(
            inclusion__icontains=search_query
        )[:10]
        data = [{'inc': ins.inclusion} for ins in inclus]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


@login_required(login_url="admin_login")
def search_ex(request):
    if 'ex_search_query' in request.GET:
        search_query = request.GET['ex_search_query']
        exclus = quotation_fill_Exclusion.objects.filter(
            exclusion__icontains=search_query
        )[:10]
        data = [{'exc': ins.exclusion} for ins in exclus]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


# For viewing existing inclusion
@csrf_protect
@login_required(login_url="admin_login")
def admin_viewQuotationInclusion(request, inclusion_id):

    try:
        inc = quotation_inclusion.objects.get(id = inclusion_id)
    except quotation_inclusion.DoesNotExist:
        return HttpResponseServerError("Selected Highlight does not exist")

    if request.method == "POST":
        try:
            if 'inclun' and 'exclu' in request.POST:
                inc.inclu = request.POST['inclun']
                inc.exclu = request.POST['exclu']

            inc.save()

            return redirect('admin_viewQuotation', inc.q_id)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))
        
    context = {"inc": inc, 'id': inclusion_id}

    return render(request, "AdminPanel/quotation/viewQuotationInclusion.html", context = context)

# for editing existing inclusion
@csrf_protect
@login_required(login_url="admin_login")
def quotation_editInclusion(request, inclusion_id):
    q_inclu = quotation_inclusion.objects.get(id=inclusion_id)
    if request.method == 'POST':    
        ins = request.POST.get('inclun')
        exclu = request.POST.get('exclu')

        q_inclu.inclu = ins
        q_inclu.exclu = exclu
        q_inclu.save()
        return redirect('admin_viewQuotation', q_inclu.q_id)

    context = {'id': inclusion_id }
    return render(request, "AdminPanel/quotation/viewQuotationInclusion.html", context)

# for deleting inclusion object
@login_required(login_url="admin_login")
def delete_quotationInclusion(request, inc_id):
    inclusion = get_object_or_404(quotation_inclusion, pk=inc_id)
    inclusion.delete()
    return redirect('admin_viewQuotation', inclusion.q_id) 



# for airlines
    
#     if request.method == 'POST':
#         id = q_id
#         ar = request.POST.get('air')

#         airlines = quotation_airlines(q_id=id, airlns=ar)
#         airlines.save()

#         return redirect('admin_viewQuotation', q_id)

#     content = {'id': q_id}
#     return render(request, "AdminPanel/quotation/addQuotation_Airlines.html", content)


@login_required(login_url="admin_login")
def search_air(request):
    if 'air_search_query' in request.GET:
        search_query = request.GET['air_search_query']
        arln = quotation_fill_Airlines.objects.filter(
            airlines__icontains=search_query
        )[:10]
        data = [{'aline': a.airlines} for a in arln]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


#     airln = get_object_or_404(quotation_airlines, pk=air_id)
#     airln.delete()
#     return redirect('admin_viewQuotation', airln.q_id) 


# for hotels

@login_required(login_url="admin_login")
def q_addHotels(request, q_id):
    
    if request.method == 'POST':
        id = q_id
        ht = request.POST.get('hotel_n')
        ar = request.POST.get('air')
        hotls = quotation_hotels(q_id=id, hotels=ht, airlns=ar)
        hotls.save()

        return redirect('admin_viewQuotation', q_id)

    content = {'id': q_id}
    return render(request, "AdminPanel/quotation/addQuotation_Hotels.html", content)



@login_required(login_url="admin_login")
def search_hotel(request):
    if 'hotel_search_query' in request.GET:
        search_query = request.GET['hotel_search_query']
        htls = quotation_fill_Hotels.objects.filter(
            hotels__icontains=search_query
        )[:10]
        data = [{'hotel_na': h.hotels} for h in htls]
        return JsonResponse(data, safe=False)
    return JsonResponse([], safe=False)


# For viewing existing Hotels
@csrf_protect
@login_required(login_url="admin_login")
def admin_viewQuotationHotels(request, hotel_id):

    try:
        htl = quotation_hotels.objects.get(id = hotel_id)
    except quotation_hotels.DoesNotExist:
        return HttpResponseServerError("Selected Highlight does not exist")

    if request.method == "POST":
        try:
            if 'hotel_n' in request.POST:
                htl.hotels = request.POST['hotel_n']
                
            if 'air' in request.POST:
                htl.airlns = request.POST.get('air')
            htl.save()

            return redirect('admin_viewQuotation', htl.q_id)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))
        
    context = {"htls": htl, 'id': hotel_id}

    return render(request, "AdminPanel/quotation/viewQuotationHotels.html", context = context)

# for editing existing Hotels
@csrf_protect
@login_required(login_url="admin_login")
def quotation_editHotels(request, hotel_id):
    q_hotel = quotation_hotels.objects.get(id=hotel_id)
    if request.method == 'POST':    
        ht = request.POST.get('hotel_n')
        air = request.POST.get('air')

        q_hotel.hotels = ht
        q_hotel.airlns = air
        q_hotel.save()
        return redirect('admin_viewQuotation', q_hotel.q_id)

    context = {'id': hotel_id }
    return render(request, "AdminPanel/quotation/viewQuotationHotels.html", context)

# for deleting Hotels objects
@login_required(login_url="admin_login")
def delete_quotationHotels(request, hotel_id):
    hotel = get_object_or_404(quotation_hotels, pk=hotel_id)
    hotel.delete()
    return redirect('admin_viewQuotation', hotel.q_id) 


# PREVIEW quotation

def preview_invoice(request, q_id):
    quotation_all = quotation.objects.filter(q_id=q_id)
    q_ity = quotation_itinerary.objects.filter(q_id=q_id)
    q_inclu = quotation_inclusion.objects.filter(q_id=q_id)
    q_hotel = quotation_hotels.objects.filter(q_id=q_id)

    

    user = request.user


    total_adult, total_child, total_infant ,total=0,0,0,0

    if quotation_all and quotation_all[0].num_adult and quotation_all[0].per_adult:
        total_adult = quotation_all[0].num_adult * quotation_all[0].per_adult
    
    if quotation_all and quotation_all[0].num_child and quotation_all[0].per_child:
        total_child = quotation_all[0].num_child * quotation_all[0].per_child

    if quotation_all and quotation_all[0].num_infant and quotation_all[0].per_infant:
        total_infant = quotation_all[0].num_infant * quotation_all[0].per_infant
    
    total = total_adult + total_infant + total_child

    content = { 'q_all': quotation_all, 'itys' : q_ity, 'inclus' : q_inclu, 'hotel' : q_hotel, 'user': user, 'adult' : total_adult, 'child': total_child, 'infant' : total_infant, 'total': total}

    return render(request, 'AdminPanel/quotation/preview_invoice.html', content)

# QUOTATION - END

@login_required(login_url="admin_login")
def delete_adminCountry(request, pk):
    country = get_object_or_404(Visa_Service_Countries, pk=pk)
    country.delete()
    return redirect(reverse("admin_visa_service"))


@login_required(login_url="admin_login")
def admin_package(request):
    package = Package.objects.all()
    return render(request, "AdminPanel/Package.html", locals())


@csrf_protect
@login_required(login_url="admin_login")
def admin_addPackage(request):
    try:
        if request.method == 'POST':
            location = request.POST.get('location', '')
            country = request.POST.get('country', '')
            duration = request.POST.get('duration', '')
            average_person = request.POST.get('average_person', '')
            accomodation = request.POST.get('accomodation', '')
            hotel_transfer = request.POST.get('hotel_transfer', '')
            visa= request.POST.get('visa', '')
            meals = request.POST.get('meals')
            airfare = request.POST.get('airfare', '')
            insurance = request.POST.get('insurance', '')
            overview = request.POST.get('overview', '')
            price = request.POST.get('price', '')
            
            location_image = request.FILES.get('location_image')

            
            package = Package(
                country_name = country,
                location_name = location,
                location_image = location_image,
                package_duration = duration,
                total_person = average_person,
                accomodation = accomodation,
                hotel_transfer = hotel_transfer,
                visa = visa,
                meals = meals,
                airfare = airfare,
                insurance_coverage = insurance,
                overview = overview,
                price = price        
            )

            package.save()
            return redirect('admin_package')

        return render(request, "AdminPanel/addPackage.html", locals())
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return HttpResponse(error_message, status=500)
    

@login_required(login_url="admin_login")
def delete_adminPackage(request, pk):
    package = get_object_or_404(Package, pk=pk)
    package.delete()
    return redirect(reverse("admin_package"))



@csrf_protect
@login_required(login_url="admin_login")
def admin_packageview(request, slug):
    try:
        package = Package.objects.get(slug=slug)
        highlight = Highlight.objects.filter(package = package.id)
        itenarary = Itinerary.objects.filter(package=package)
        inclusion = Inclusion.objects.filter(package=package)
        exclusion = Exclusion.objects.filter(package=package)

        if request.method == 'POST':
            print("Posted")
            try:       
                package.location_name = request.POST.get('location')
                package.country_name = request.POST.get('country',)
                package.package_duration = request.POST.get('duration',)
                package.total_person = request.POST.get('average_person',)
                package.accomodation = request.POST.get('accomodation',)
                package.hotel_transfer = request.POST.get('hotel_transfer',)
                package.visa= request.POST.get('visa',)
                package.meals = request.POST.get('meals')
                package.airfare = request.POST.get('airfare',)
                package.insurance_coverage = request.POST.get('insurance',)
                package.overview = request.POST.get('overview',)
                package.price= request.POST.get('price',)
                package.is_featured = request.POST.get('is_featured') == 'on'
                
                if request.FILES.get('location_image'):
                    package.location_image = request.FILES['location_image']
                
                package.save()
                return redirect('admin_package')
            except Exception as e:
                error_message = str(e)
                return render(request, 'AdminPanel/viewPackage.html', {'error': error_message, 'package': package, 'highlight': highlight, 'inclusion': inclusion, 'exclusion': exclusion, 'itinerary': itenarary})
                
                # return HttpResponseServerError('An error occurred: {}'.format(str(e)))
            
        context = {
            'package': package,
            'highlight': highlight,
            'inclusion': inclusion,
            'exclusion': exclusion,
            'itinerary': itenarary
            }
        
        print("rendered")
        return render(request, "AdminPanel/viewPackage.html", context=context)
    
    except Package.DoesNotExist:
        return HttpResponseServerError("Package does not exist")


@csrf_protect
@login_required(login_url="admin_login")
def search_packages(request):
     if request.method == "POST":
        query = request.POST.get("pack-query")
        pack = Package.objects.filter(Q(country_name__icontains=query) | Q(location_name__icontains=query))
    
        return render(request, "AdminPanel/Package.html", locals())

@csrf_protect
@login_required(login_url="admin_login")
def admin_viewaddpackagehighlight(request, package_id):
    package = Package.objects.get(id=package_id)
    if request.method == 'POST':    
        highlight = request.POST.get('highlight')
        package_highlight = Highlight(package=package, highlight= highlight)
        package_highlight.save()
        return redirect('admin_viewPackage', slug=package.slug)
    context = {'id': package_id }
    return render(request, "AdminPanel/addPackageHighlight.html", context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewaddpackageItenerary(request, package_id):
    package = Package.objects.get(id=package_id)
    if request.method == 'POST':    
        title = request.POST.get('title')
        description = request.POST.get('description')
        package_itenerary = Itinerary(package=package, title=title, description=description)
        package_itenerary.save()
        return redirect('admin_viewPackage', slug=package.slug)
    context = {'id': package_id }
    return render(request, "AdminPanel/addPackageItenerary.html", context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewaddpackageInclusion(request, package_id):
    package = Package.objects.get(id=package_id)
    if request.method == 'POST':    
        inclusion = request.POST.get('inclusion')
        package_inclusion = Inclusion(package=package, inclusion=inclusion)
        package_inclusion.save()
        return redirect('admin_viewPackage', slug=package.slug)
    context = {'id': package_id }
    return render(request, "AdminPanel/addPackageInclusion.html", context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewaddpackageExclusion(request, package_id):
    package = Package.objects.get(id=package_id)
    if request.method == 'POST':    
        exclusion = request.POST.get('exclusion')
        package_exclusion = Exclusion(package=package, exclusion=exclusion)
        package_exclusion.save()
        return redirect('admin_viewPackage', slug=package.slug)
    context = {'id': package_id }
    return render(request, "AdminPanel/addPackageExclusion.html", context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewHighlight(request, package_id):
    try:
        highlight = Highlight.objects.get(id = package_id)
    except Highlight.DoesNotExist:
        return HttpResponseServerError("Selected Highlight does not exist")

    if request.method == "POST":
        try:
            if 'highlight' in request.POST:
                highlight.highlight = request.POST['highlight']
            
            highlight.save()

            return redirect('admin_viewPackage', slug=highlight.package.slug)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"h": highlight, 'id': package_id}

    return render(request, "AdminPanel/viewPackageHighlight.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewItinerary(request, package_id):
    try:
        itinerary = Itinerary.objects.get(id = package_id)
    except Itinerary.DoesNotExist:
        return HttpResponseServerError("Selected Itinerary does not exist")

    if request.method == "POST":
        try:
            if 'title' in request.POST:
                itinerary.title = request.POST['title']
            
            if 'description' in request.POST:
                itinerary.description = request.POST['description']
            
            
            itinerary.save()

            return redirect('admin_viewPackage', slug=itinerary.package.slug)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": itinerary, 'id': package_id}

    return render(request, "AdminPanel/viewPackageItinerary.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewInclusion(request, package_id):
    try:
        inclusion = Inclusion.objects.get(id = package_id)
    except Inclusion.DoesNotExist:
        return HttpResponseServerError("Selected Inclusion does not exist")

    if request.method == "POST":
        try:
            if 'inclusion' in request.POST:
                inclusion.inclusion = request.POST['inclusion']
            
            inclusion.save()

            return redirect('admin_viewPackage', slug=inclusion.package.slug)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": inclusion, 'id': package_id}

    return render(request, "AdminPanel/viewPackageInclusion.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewExclusion(request, package_id):
    try:
        exclusion = Exclusion.objects.get(id = package_id)
    except Exclusion.DoesNotExist:
        return HttpResponseServerError("Selected Inclusion does not exist")

    if request.method == "POST":
        try:
            if 'exclusion' in request.POST:
                exclusion.exclusion = request.POST['exclusion']
            
            exclusion.save()

            return redirect('admin_viewPackage', slug=exclusion.package.slug)
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": exclusion, 'id': package_id}

    return render(request, "AdminPanel/viewPackageExclusion.html", context = context)


@login_required(login_url="admin_login")
def delete_adminProductHighlight(request, pk):
    highlight = get_object_or_404(Highlight, pk=pk)
    highlight.delete()
    return redirect('admin_viewPackage', slug=highlight.package.slug)


@login_required(login_url="admin_login")
def delete_adminProductItinerary(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk)
    itinerary.delete()
    return redirect('admin_viewPackage', slug=itinerary.package.slug)


@login_required(login_url="admin_login")
def delete_adminProductInclusion(request, pk):
    inclusion = get_object_or_404(Inclusion, pk=pk)
    inclusion.delete()
    return redirect('admin_viewPackage', slug=inclusion.package.slug)


@login_required(login_url="admin_login")
def delete_adminProductExclusion(request, pk):
    exclusion = get_object_or_404(Exclusion, pk=pk)
    exclusion.delete()
    return redirect('admin_viewPackage', slug=exclusion.package.slug)


#FLight Request
@login_required(login_url="admin_login")
def admin_flightRequest(request):
    flight = Flight_request.objects.all().order_by('-Date')
    return render(request, 'AdminPanel/FlightRequest.html', locals())


# Search for flight request
@csrf_protect
@login_required(login_url="admin_login")
def search_flight_request(request):
    if request.method == "POST":
        query = request.POST.get("flight-query")

        req = Flight_request.objects.filter(Q(client_name__icontains=query)| Q(client_phone__icontains=query) | Q(client_email__icontains=query)| Q(departure__icontains=query)| Q(destination__icontains=query)| Q(Date__icontains=query))
    
        return render(request, "AdminPanel/FlightRequest.html", locals())


@login_required(login_url="admin_login")
def admin_viewflightRequest(request, pk):
    i = get_object_or_404(Flight_request, pk=pk)
    return render(request, 'AdminPanel/viewFlightRequest.html', locals())


@login_required(login_url="admin_login")
def delete_adminflightrequest(request, pk):
    flight = get_object_or_404(Flight_request, pk=pk)
    flight.delete()
    return redirect('admin_flightrequest')


@login_required(login_url="admin_login")
def admin_inquiry(request):
    inquiry = new_contact.objects.all().order_by('-Date')
    return render(request, 'AdminPanel/Inquiry.html', locals())


@csrf_protect
@login_required(login_url="admin_login")
def search_inquiry(request):
    if request.method == "POST":
        query = request.POST.get("inq-query")
        inq = new_contact.objects.filter(Q(client_name__icontains=query) | Q(client_contact__icontains=query) | Q(Date__icontains=query))
    
        return render(request, "AdminPanel/inquiry.html", locals())
    

@login_required(login_url="admin_login")
def admin_viewInquiry(request, pk):
    i = get_object_or_404(new_contact, pk=pk)
    return render(request, 'AdminPanel/viewInquiry.html', locals())


@login_required(login_url="admin_login")
def delete_adminInquiry(request, pk):
    i = get_object_or_404(new_contact, pk=pk)
    i.delete()
    return redirect('admin_inquiry')


@login_required(login_url="admin_login")
def admin_poster(request):
    poster = deals_event.objects.all()
    return render(request, 'AdminPanel/Events.html', locals())


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewPoster(request, pk):
    try:
        poster = deals_event.objects.get(pk=pk)
    except Visa_Service_Countries.DoesNotExist:
        return HttpResponseServerError("Event poster does not exist")

    if request.method == "POST":
        try:
            if 'title' in request.POST:
                poster.deal_title = request.POST['title']
            if 'poster' in request.FILES:
                poster.deal_poster = request.FILES['poster']
            if 'deal_url' in request.POST:
                poster.deal_url = request.POST['deal_url']

            poster.save()

            return redirect('admin_poster')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"poster": poster}

    return render(request, "AdminPanel/viewPoster.html", context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_addPoster(request):
    if request.method == 'POST':
        deal_title = request.POST.get('title')  
        deal_poster = request.FILES.get('poster') 
        deal_url = request.POST.get('deal_url') 
        poster = deals_event(deal_title=deal_title, deal_poster=deal_poster,deal_url=deal_url)
        poster.save()

        return redirect('admin_poster') 
    return render(request, "AdminPanel/addPoster.html", locals())


@login_required(login_url="admin_login")
def delete_adminPoster(request, pk):
    i = get_object_or_404(deals_event, pk=pk)
    i.delete()
    return redirect('admin_poster')
    
    
@login_required(login_url="admin_login")
def admin_user(request):
    user = Company_Members.objects.all()
    return render(request, 'AdminPanel/user.html', locals())


# Search Users
@csrf_protect
@login_required(login_url="admin_login")
def search_members(request):
    if request.method == "POST":
        query = request.POST.get("user-query")
        us = Company_Members.objects.filter(Q(full_name__icontains = query) | Q(contact__icontains = query)| Q(join_date__icontains = query))
    
        return render(request, "AdminPanel/user.html", locals())


@login_required(login_url="admin_login")
def admin_addUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        full_name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        position = request.POST.get('position')
        blood_group = request.POST.get('blood_group')
        address = request.POST.get('address')
        join_date = request.POST.get('join_date')
        card_expire = request.POST.get('card_expire')
        is_admin = request.POST.get('is_admin') == 'on'
        is_member = request.POST.get('is_member') == 'on'
        is_active = request.POST.get('is_active') == 'on'
        user_image = request.FILES.get('user_image')

        # Save user data to the database
        user = Company_Members.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            contact=contact,
            position=position,
            blood_group=blood_group,
            address=address,
            join_date=join_date,
            card_expiration_date=card_expire,
            is_admin=is_admin,
            is_member=is_member,
            is_active=is_active,
            profile=user_image
        )

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        member_url = reverse('staff_detail', kwargs={'slug': user.slug})
        website_url = 'https://flightmandu.com.np'
        qr.add_data(website_url + member_url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        image_data = buffer.getvalue()
        user.qr_code.save(f'{user.slug}_qr_code.png', ContentFile(image_data), save=False)

        messages.success(request, 'User registered successfully!')
        return redirect('admin_user')
    return render(request, 'AdminPanel/RegisterUser.html')



@login_required(login_url="admin_login")
def admin_viewUser(request, slug):
    user = get_object_or_404(Company_Members, slug=slug)

    if request.method == 'POST':
        try:   
            user.username = request.POST.get('username')
            user.full_name = request.POST.get('name')
            user.contact = request.POST.get('contact')
            user.position = request.POST.get('position')
            user.blood_group = request.POST.get('blood_group')
            user.address = request.POST.get('address')
            user.join_date = request.POST.get('join_date')
            user.card_expiration_date = request.POST.get('card_expire')
            user.is_admin = request.POST.get('is_admin') == 'on'
            user.is_member = request.POST.get('is_member') == 'on'
            user.is_active = request.POST.get('is_active') == 'on'
            user_image = request.FILES.get('user_image')

            if user_image:
                user.profile = user_image

            user.save()

            messages.success(request, 'User details updated successfully!')
            return redirect('admin_user') 
        except Exception as e:
                error_message = str(e)
                return render(request, 'AdminPanel/viewUser.html', {'error': error_message, 'user': user })
                
    
    return render(request, 'AdminPanel/viewUser.html', {'user': user})


@login_required(login_url="admin_login")
def admin_deleteUser(request, pk):
    i = get_object_or_404(Company_Members, pk=pk)
    i.delete()
    return redirect('admin_user')


@login_required(login_url="admin_login")
def admin_fill_data(request):
    itinerary = quotation_fill_Itinerary.objects.all()
    meals = quotation_fill_Meals.objects.all()
    inclusion = quotation_fill_Inclusion.objects.all()
    hotels = quotation_fill_Hotels.objects.all()
    airlines = quotation_fill_Airlines.objects.all()
    exclusion = quotation_fill_Exclusion.objects.all()
    return render(request, 'AdminPanel/fill_data.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_itinerary(request):
    if request.method == 'POST': 
        i = request.POST.get('itinerary')
        itinerary = quotation_fill_Itinerary(itinerary = i)
        itinerary.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_itinerary.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_meals(request):
    if request.method == 'POST': 
        i = request.POST.get('meals')
        meals = quotation_fill_Meals(meals = i)
        meals.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_meals.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_inclusion(request):
    if request.method == 'POST': 
        i = request.POST.get('inclusion')
        inclusion = quotation_fill_Inclusion(inclusion = i)
        inclusion.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_inclusion.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_exclusion(request):
    if request.method == 'POST': 
        i = request.POST.get('exclusion')
        exclusion = quotation_fill_Exclusion(exclusion = i)
        exclusion.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_exclusion.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_hotels(request):
    if request.method == 'POST': 
        i = request.POST.get('hotels')
        hotels = quotation_fill_Hotels(hotels = i)
        hotels.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_hotels.html', locals())


@login_required(login_url="admin_login")
def admin_addFill_airlines(request):
    if request.method == 'POST': 
        i = request.POST.get('airlines')
        airlines = quotation_fill_Airlines(airlines = i)
        airlines.save()
        return redirect('admin_fill_data')
    return render(request, 'AdminPanel/addFill_airlines.html', locals())


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_itinerary(request, pk):
    try:
        i = quotation_fill_Itinerary.objects.get(id = pk)
    except quotation_fill_Itinerary.DoesNotExist:
        return HttpResponseServerError("Selected Highlight does not exist")

    if request.method == "POST":
        try:
            if 'itinerary' in request.POST:
                i.itinerary = request.POST['itinerary']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_itinerary.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_meals(request, pk):
    try:
        i = quotation_fill_Meals.objects.get(id = pk)
    except quotation_fill_Meals.DoesNotExist:
        return HttpResponseServerError("Selected meals does not exist")

    if request.method == "POST":
        try:
            if 'meals' in request.POST:
                i.meals = request.POST['meals']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_meals.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_inclusion(request, pk):
    try:
        i = quotation_fill_Inclusion.objects.get(id = pk)
    except quotation_fill_Inclusion.DoesNotExist:
        return HttpResponseServerError("Selected Inclusion does not exist")

    if request.method == "POST":
        try:
            if 'inclusion' in request.POST:
                i.inclusion = request.POST['inclusion']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_inclusion.html", context = context)


@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_exclusion(request, pk):
    try:
        i = quotation_fill_Exclusion.objects.get(id = pk)
    except quotation_fill_Exclusion.DoesNotExist:
        return HttpResponseServerError("Selected Exclusion does not exist")

    if request.method == "POST":
        try:
            if 'exclusion' in request.POST:
                i.exclusion = request.POST['exclusion']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_exclusion.html", context = context)




@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_hotels(request, pk):
    try:
        i = quotation_fill_Hotels.objects.get(id = pk)
    except quotation_fill_Hotels.DoesNotExist:
        return HttpResponseServerError("Selected Inclusion does not exist")

    if request.method == "POST":
        try:
            if 'hotels' in request.POST:
                i.hotels = request.POST['hotels']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_hotels.html", context = context)



@csrf_protect
@login_required(login_url="admin_login")
def admin_viewFill_airlines(request, pk):
    try:
        i = quotation_fill_Airlines.objects.get(id = pk)
    except quotation_fill_Airlines.DoesNotExist:
        return HttpResponseServerError("Selected Airline does not exist")

    if request.method == "POST":
        try:
            if 'airlines' in request.POST:
                i.airlines = request.POST['airlines']
            
            i.save()

            return redirect('admin_fill_data')
        except Exception as e:
            return HttpResponseServerError('An error occurred: {}'.format(str(e)))

    context = {"i": i}

    return render(request, "AdminPanel/viewFill_airlines.html", context = context)


@login_required(login_url="admin_login")
def delete_adminFillItinerary(request, pk):
    i = get_object_or_404(quotation_fill_Itinerary, pk=pk)
    i.delete()
    return redirect('admin_fill_data')

@login_required(login_url="admin_login")
def delete_adminFillInclusion(request, pk):
    i = get_object_or_404(quotation_fill_Inclusion, pk=pk)
    i.delete()
    return redirect('admin_fill_data')


@login_required(login_url="admin_login")
def delete_adminFillExclusion(request, pk):
    i = get_object_or_404(quotation_fill_Exclusion, pk=pk)
    i.delete()
    return redirect('admin_fill_data')

@login_required(login_url="admin_login")
def delete_adminFillMeals(request, pk):
    i = get_object_or_404(quotation_fill_Meals, pk=pk)
    i.delete()
    return redirect('admin_fill_data')

@login_required(login_url="admin_login")
def delete_adminFillHotels(request, pk):
    i = get_object_or_404(quotation_fill_Hotels, pk=pk)
    i.delete()
    return redirect('admin_fill_data')

@login_required(login_url="admin_login")
def delete_adminFillAirlines(request, pk):
    i = get_object_or_404(quotation_fill_Airlines, pk=pk)
    i.delete()
    return redirect('admin_fill_data')


@login_required(login_url="admin_login")
def businessSetting(request):
    try:
        info = BusinessInfo.objects.all().first()
    except BusinessInfo.DoesNotExist:
        return HttpResponseServerError("Business data do not exist")
    

    if request.method == 'POST':
        # Handle form submission
        info.Business_Name = request.POST.get('name', '')
        info.Business_bio = request.POST.get('bio', '')
        info.Business_Contact = request.POST.get('contact', '')
        info.Business_Email = request.POST.get('email', '')
        info.Business_Address = request.POST.get('location', '')
        info.Business_Opening_Time = request.POST.get('time', '')
        info.Facebook_Link = request.POST.get('facebook', '')
        info.Instagram_Link = request.POST.get('instagram', '')
        info.Whatsapp_Link = request.POST.get('whatsapp', '')
        info.About_us = request.POST.get('about', '')
        info.TermsConditions = request.POST.get('terms', '')

        # Handle file uploads
        if 'upload1' in request.FILES:
            info.Business_Logo = request.FILES['upload1']
        
        # Save the updated information
        info.save()

    context = {'info': info}
    return render(request, "AdminPanel/businessSetting.html", context=context)

from django.contrib.auth.hashers import make_password

@login_required(login_url="admin_login")
def change_password(request, slug):
    user = Company_Members.objects.get(slug=slug)
    
    if request.method == 'POST':
        new_password = request.POST.get('pass')
        print(new_password)
        user.password = make_password(new_password)
        
        user.save()
        return redirect('admin_viewUser', slug= user.slug)
    
    return render(request, 'AdminPanel/changepassword.html', locals())

    
    






