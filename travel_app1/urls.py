from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='home'),
    path('main/', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('send/', views.send_message, name='send'),
    path('request_flight/', views.request_flight, name="request_flight"),
    path('terms&condition/', views.policy, name="policy"),
    path('about/', views.about, name="about"),
    path('search/', views.search_airports, name='search_airports'),
    path('visa_service/', views.visaService, name="visa"),
    path('package/', views.packages, name = "package"),
    path('package/<slug:slug>', views.package_detail, name="package_detail"),
 
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)