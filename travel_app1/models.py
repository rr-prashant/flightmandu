from django.db import models
from django.db.models.signals import pre_save
from travel_app1.package_slug import unique_slug_generator

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
    Adult = models.CharField(max_length=100, null=True, blank=True) 
    Children = models.CharField(max_length=100, null=True, blank=True) 
    Infant = models.CharField(max_length=100, null=True, blank=True)
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
    country_name = models.CharField(max_length=200, blank=True, null = True)
    location_name = models.CharField(max_length=200, blank=True, null = True)
    location_image = models.ImageField(upload_to='packages_image', blank=True, null=True)
    location_desc = models.CharField(max_length=200, blank=True, null = True)
    package_duration = models.IntegerField(blank=True, null=True)
    total_person = models.IntegerField(blank=True, null=True)
    accomodation = models.CharField(max_length=200, blank=True, null = True)
    hotel_transfer = models.CharField(max_length=200, blank=True, null = True)
    visa = models.CharField(max_length=200, blank=True, null = True)
    meals = models.CharField(max_length=200, blank=True, null = True)
    airfare = models.CharField(max_length=200, blank=True, null = True)
    insurance_coverage = models.CharField(max_length=200, blank=True, null = True)
    overview = models.TextField(null=True, blank=True)
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
    
    
    