from io import BytesIO
from django.db import models
from django.db.models.signals import pre_save
from travel_app1.package_slug import unique_slug_generator
from travel_app1.member_slug import unique_member_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
import qrcode
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.utils.translation import gettext_lazy as _
from travel_app1.Qid_generator import unique_quotation_id_generator
              
class Company_Members(AbstractUser):
    full_name = models.CharField(max_length=300, blank=False, null = False)
    contact = models.CharField(max_length=300, blank=False, null = False)
    position = models.CharField(max_length=300, blank=False, null = False)
    blood_group = models.CharField(max_length=300, blank=False, null = False)
    address = models.CharField(max_length=300, blank=False, null = False)
    join_date = models.DateField(blank=True, null=True)
    profile = models.ImageField(upload_to='profile', blank=True)
    card_expiration_date = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True, blank=True, editable=True)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_users',  # Add a related_name here
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_users',  # Add a related_name here
        related_query_name='custom_user',
    )
    
    def __str__(self):
        return self.username
    
@receiver(pre_save, sender=Company_Members)
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_member_slug_generator(instance)
        
    if not instance.qr_code:
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        
        member_url = reverse('staff_detail', kwargs={'slug': instance.slug}) 
        website_url = 'https://flightmandu.com.np' 
        qr.add_data(website_url + member_url)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")
    
        buffer = BytesIO()
        qr_image.save(buffer, format='PNG')
        image_data = buffer.getvalue()

        instance.qr_code.save(f'{instance.slug}_qr_code.png', ContentFile(image_data), save=False)

    
class BusinessInfo(models.Model):
    Business_Name = models.CharField(max_length=100, null=False, blank=False)
    Business_bio = models.TextField(null=True, blank=True)
    Business_Logo = models.ImageField(null=False, blank=False)
    Business_Contact = models.CharField(max_length=100, null=False, blank=False)
    Business_Email = models.CharField(max_length=100, null=False, blank=False)
    Business_Opening_Time = models.CharField(max_length=100, null=False, blank=False)
    Business_Address = models.CharField(max_length=100, null=False, blank=False)
    Facebook_Link =   models.CharField(max_length=500, null=True, blank=True)
    Instagram_Link =   models.CharField(max_length=500, null=True, blank=True)
    Whatsapp_Link =   models.CharField(max_length=500, null=True, blank=True)
    About_us = models.TextField(null=True, blank=True)
    TermsConditions = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.Business_Name

class Flight_request(models.Model):
    client_name = models.CharField(max_length=100, null=False, blank=False)
    client_email = models.CharField(max_length=100, null=False, blank=False)
    client_phone = models.CharField(max_length=100, null=False, blank=False)
    departure = models.CharField(max_length=100, null=False, blank=False)
    destination = models.CharField(max_length=100, null=False, blank=False)
    departure_date = models.CharField(max_length=100, null=False, blank=False)
    Round_trip = models.BooleanField(default=False)
    return_date = models.CharField(max_length=100, default='N/A', null=True, blank=True)
    Adult = models.CharField(max_length=100, default='0', null=True, blank=True) 
    Children = models.CharField(max_length=100, default='0',  null=True, blank=True) 
    Infant = models.CharField(max_length=100, default='0', null=True, blank=True)
    Date = models.DateField(auto_now_add=True, blank=True) 
    
    def __str__(self):
        return self.client_name
    
    class Meta:
        verbose_name = "Customer Flight Request"  
        verbose_name_plural = "Customer Flight Request"


class new_contact(models.Model):
    client_name = models.CharField(max_length=100, null=False, blank=False)
    client_contact = models.CharField(max_length=100, null=False, blank=False)
    client_subject = models.CharField(max_length=100, null=True, blank=True)  
    client_message = models.TextField(null=True, blank=True) 
    Date = models.DateField(auto_now_add=True, blank=True) 

    def __str__(self):
        return self.client_name
    
    class Meta:
        verbose_name = "Customer Inquiries"  
        verbose_name_plural = "Customer Inquiries"
    
    
class Airport(models.Model):
    name = models.CharField(max_length=200)
    location_name = models.CharField(max_length=200)  # Add field for location name
    country = models.CharField(max_length=200, blank=True, null = True)
    iata_code = models.CharField(max_length=200, blank=True, null = True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
    
class Visa_Service_Countries(models.Model):
    country_name = models.CharField(max_length=200, blank=True, null = True)
    country_flag = models.ImageField(upload_to='country_flag', blank=True, null=True)

    def __str__(self):
        return self.country_name
    
class Package(models.Model):
    country_name = models.CharField(max_length=200, blank=False, null = True)
    location_name = models.CharField(max_length=200, blank=False, null = True)
    location_image = models.ImageField(upload_to='packages_image', blank=False, null=True)
    package_duration = models.IntegerField(blank=True, null=True)
    total_person = models.IntegerField(blank=True, null=True)
    accomodation = models.CharField(max_length=200, blank=True, null = True)
    hotel_transfer = models.CharField(max_length=200, blank=True, null = True)
    visa = models.CharField(max_length=200, blank=True, null = True)
    meals = models.CharField(max_length=200, blank=True, null = True)
    airfare = models.CharField(max_length=200, blank=True, null = True)
    insurance_coverage = models.CharField(max_length=200, blank=True, null = True)
    overview = models.TextField(null=True, blank=True)
    is_featured = models.BooleanField(null=False, blank=False, default=False)
    price = models.TextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True, editable=True)
    
    def __str__(self):
        return self.location_name
    
def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(pre_save_receiver, sender=Package)



class deals_event(models.Model):
    deal_title = models.CharField(max_length=300, blank=True, null = True)
    deal_poster = models.ImageField(upload_to='poster', blank=True, null=True)
    deal_url = models.CharField(max_length=1000, blank=True, null = True)
    
    def __str__(self):
        return self.deal_title
    
    class Meta:
        verbose_name = "Event Posters"  
        verbose_name_plural = "Event Posters"
    
    
class Itinerary(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=300, blank=True, null = True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.package.location_name + ": " + self.title
    
    class Meta:
        verbose_name = "Package Itinerary"  
        verbose_name_plural = "Package Itinerary"
    
    
class Highlight(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    highlight = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.package.location_name + ": " + self.highlight
    
    class Meta:
        verbose_name = "Package Highlights"  
        verbose_name_plural = "Package Highlights"
    

class Inclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    inclusion = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return self.package.location_name + ": " + self.inclusion
    
    class Meta:
        verbose_name = "Package Inclusions"  
        verbose_name_plural = "Package Inclusions"
    

class Exclusion(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True)
    exclusion = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.package.location_name + ": " + self.exclusion
    
    class Meta:
        verbose_name = "Package Exclusions"  
        verbose_name_plural = "Package Exclusions"
        
        
class quotation(models.Model):
    q_id = models.IntegerField(null=True, blank=True, editable=True)
    client_name = models.CharField(max_length=100, blank=True, null = True)
    client_phone = models.CharField(max_length=10, blank=True, null = True)
    client_email = models.CharField(max_length=300, blank=True, null = True)
    package_name = models.CharField(max_length=1000, blank=True, null = True)
    per_adult = models.IntegerField(blank=True, null=True)
    per_child = models.IntegerField(blank=True, null=True)
    per_infant = models.IntegerField(blank=True, null=True)
    q_Date = models.DateField(auto_now_add=True, blank=True) 
    num_adult = models.IntegerField(blank=True, null=True, default=0)
    num_child = models.IntegerField(blank=True, null=True, default=0)
    num_infant = models.IntegerField(blank=True, null=True, default=0)
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name

def pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.q_id:
        instance.q_id = unique_quotation_id_generator(instance)
    
pre_save.connect(pre_save_receiver, sender=quotation)

class quotation_fill_Inclusion(models.Model):
    inclusion = models.TextField(null=False, blank=False)

class quotation_fill_Exclusion(models.Model):
    exclusion = models.TextField(null=False, blank=False)

class quotation_fill_Itinerary(models.Model):
    itinerary = models.TextField(null=False, blank=False)
    
class quotation_fill_Hotels(models.Model):
    hotels = models.TextField(null=False, blank=False)
    
class quotation_fill_Meals(models.Model):
    meals = models.TextField(null=False, blank=False)

    
class quotation_fill_Airlines(models.Model):
    airlines = models.TextField(null=False, blank=False)
    

# Iterary table data model 
class quotation_itinerary(models.Model):
    q_id = models.IntegerField(null=True, blank=True, editable=True)
    date = models.DateField(null=True, blank=True)
    day = models.IntegerField(null=True, blank=True)
    Itinerary = models.TextField(null=True, blank=True)
    Meals = models.TextField(max_length=1000, null=True, blank=True)
        
    def __str__(self):
        return str(self.q_id)
    
# Inclusion table data model
class quotation_inclusion(models.Model):
    q_id = models.IntegerField(null=True, blank=True, editable=True)
    inclu = models.TextField(null=True, blank=True)
    exclu = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.q_id
    
    class Meta:
        verbose_name = "Quotation Inclusion and Exclusion"  
        verbose_name_plural = "Quotation Inclusions and Exclusions"
    
# Airlines table data model
class quotation_airlines(models.Model):
    q_id = models.IntegerField(null=True, blank=True, editable=True)
    airlns = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.q_id
    
# Hotels table data model
class quotation_hotels(models.Model):
    q_id = models.IntegerField(null=True, blank=True, editable=True)
    hotels = models.TextField(null=True, blank=True)
    airlns = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.q_id
    