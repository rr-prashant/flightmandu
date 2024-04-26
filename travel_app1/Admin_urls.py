from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", admin_login, name="admin_login"),
    path("visa_service/", admin_visa, name='admin_visa_service'),
    path("Log-out/", admin_signout, name="admin_logout"),
    path("add_country/", admin_addcountry, name="admin_addcountry"),
    path("delete_country/<int:pk>", delete_adminCountry, name = "admin_deletecountry"),
    path("visa_service/<int:pk>", admin_viewCountry, name = "admin_viewCountry"),
    path("package/", admin_package, name="admin_package"),
    path("add_package/", admin_addPackage, name="admin_addPackage"),
    path("delete_package/<int:pk>", delete_adminPackage, name = "admin_deletepackage"),
    path('package/<slug:slug>', admin_packageview, name="admin_viewPackage"),
    path('package/addHighlight/<int:package_id>/', admin_viewaddpackagehighlight, name='admin_addhighlight'),
    path('package/addItinerary/<int:package_id>/', admin_viewaddpackageItenerary, name='admin_addItenerary'),    
    path('package/addInclusion/<int:package_id>/', admin_viewaddpackageInclusion, name='admin_addInclusion'),    
    path('package/addExclusion/<int:package_id>/', admin_viewaddpackageExclusion, name='admin_addExclusion'),
    path('package/viewHighlight/<int:package_id>/', admin_viewHighlight, name='admin_viewHighlight'),    
    path('package/viewItinerary/<int:package_id>/', admin_viewItinerary, name='admin_viewItinerary'),    
    path('package/viewInclusion/<int:package_id>/', admin_viewInclusion, name='admin_viewInclusion'),    
    path('package/viewExclusion/<int:package_id>/', admin_viewExclusion, name='admin_viewExclusion'),
    path("DeletePackageHighlight/<int:pk>/", delete_adminProductHighlight, name="admin_deletepackagehighlight"),
    path("DeletePackageItinerary/<int:pk>/", delete_adminProductItinerary, name="admin_deletepackageitinerary"),
    path("DeletePackageInclusion/<int:pk>/", delete_adminProductInclusion, name="admin_deletepackageinclusion"),    
    path("DeletePackageExclusion/<int:pk>/", delete_adminProductExclusion, name="admin_deletepackageexclusion"),
    path("flight_request", admin_flightRequest, name = "admin_flightrequest"),
    path("flight_request/<int:pk>", admin_viewflightRequest, name = "admin_viewflightrequest"),
    path('Delete_FlightRequest/<int:pk>', delete_adminflightrequest, name = "admin_deleteflightrequest"),
    path('Inquiry/', admin_inquiry, name = "admin_inquiry"),
    path("Inquiry/<int:pk>", admin_viewInquiry, name = "admin_viewInquiry"),
    path("DeleteInquiry/<int:pk>", delete_adminInquiry, name = "admin_deleteInquiry"),
    path('poster/', admin_poster, name = "admin_poster"),
    path('poster/<int:pk>', admin_viewPoster, name = "admin_viewPoster"),
    path("add_Poster/", admin_addPoster, name="admin_addPoster"),
    path('Delete_poster/<int:pk>', delete_adminPoster, name = "admin_deletePoster"),
    path('employee/', admin_user, name="admin_user"),
    path('Register_User/', admin_addUser, name = "admin_addUser"),
    path('employee/<slug:slug>', admin_viewUser, name="admin_viewUser"),
    path('delete_employee/<int:pk>', admin_deleteUser, name = "admin_deleteUser"),
    path('fill_data/', admin_fill_data, name = "admin_fill_data"),
    path('add_fill_itinerary/', admin_addFill_itinerary, name = "admin_add_fill_itinerary"),
    path('add_fill_meals/', admin_addFill_meals, name = "admin_add_fill_meals"),
    path('add_fill_inclusion/', admin_addFill_inclusion, name = "admin_add_fill_inclusion"),
    path('add_fill_hotels/', admin_addFill_hotels, name = "admin_add_fill_hotels"),
    path('add_fill_airlines/', admin_addFill_airlines, name = "admin_add_fill_airlines"),
    path('view_fill_itinerary/<int:pk>', admin_viewFill_itinerary, name = "admin_view_fill_itinerary"),
    path('view_fill_meals/<int:pk>', admin_viewFill_meals, name = "admin_view_fill_meals"),
    path('view_fill_inclusion/<int:pk>', admin_viewFill_inclusion, name = "admin_view_fill_inclusion"),
    path('view_fill_hotels/<int:pk>', admin_viewFill_hotels, name = "admin_view_fill_hotels"),
    path('view_fill_airlines/<int:pk>', admin_viewFill_airlines, name = "admin_view_fill_airlines"),
    path('delete_fill_itinerary/<int:pk>', delete_adminFillItinerary, name = "admin_Fill_itinerary_delete"),
    path('delete_fill_meals/<int:pk>', delete_adminFillMeals, name = "admin_Fill_meals_delete"),
    path('delete_fill_inclusion/<int:pk>', delete_adminFillInclusion, name = "admin_Fill_inclusion_delete"),
    path('delete_fill_hotels/<int:pk>', delete_adminFillHotels, name = "admin_Fill_hotels_delete"),
    path('delete_fill_airlines/<int:pk>', delete_adminFillAirlines, name = "admin_Fill_airlines_delete"),
    path('business_settings/', businessSetting, name ="businessSettings"),

    # quotation
    path('quotation/add_quotation/', add_quotation, name="admin_addQuotation"),
    path('edit_quotation/<int:q_id>', editquotation ,name="admin_editquotation"),
    path('quotation/<int:q_id>',admin_viewQuotation ,name="admin_viewQuotation"),
    path('quotation/additinerary/<int:q_id>', q_addItinerary, name="q-add-itinerary" ),
    path('quotation/addinclusion/<int:q_id>', q_addinclusion, name="q-add-inclusion" ),
    # path('quotation/addairlines/<int:q_id>', q_addAirlines, name="q-add-airlines" ),
    path('quotation/addhotels/<int:q_id>', q_addHotels, name="q-add-hotels" ),


    #quotation searchbar
    path('quotation/search_invoice/', search_q , name="search_invoice"),

    #edit quotation
    #----itinerary
    path('quotation/viewItinerary/<int:itinerary_id>/', admin_viewQuotationItinerary, name='admin_viewQuotationItinerary'),
    path('quotation/editItinerary/<int:itinerary_id>/', quotation_editItenerary, name='q-edit-itinerary'), 

    #---inclusion
    path('quotation/viewInclusion/<int:inclusion_id>/', admin_viewQuotationInclusion, name='admin_viewQuotationInclusion'),
    path('quotation/editInclusion/<int:inclusion_id>/', quotation_editInclusion, name='q-edit-inclusion'), 

    #---hotel
    path('quotation/viewHotels/<int:hotel_id>/', admin_viewQuotationHotels, name='admin_viewQuotationHotels'),
    path('quotation/editHotels/<int:hotel_id>/', quotation_editHotels, name='q-edit-hotels'),

    #---airlines
    # path('quotation/viewAirlines/<int:air_id>/', admin_viewQuotationAirlines, name='admin_viewQuotationAirlines'),
    # path('quotation/editAirlines/<int:air_id>/', quotation_editAirlines, name='q-edit-airlines'),

    #delete quotation
    path("DeleteQuotationItinerary/<int:ity_id>/", delete_quotationItinerary, name="admin_deleteQuotationItinerary"),
    path("DeleteQuotationInclusion/<int:inc_id>/", delete_quotationInclusion, name="admin_deleteQuotationInclusion"),
    path("DeleteQuotationHotels/<int:hotel_id>/", delete_quotationHotels, name="admin_deleteQuotationHotels"),
    path("delete_quotation/<int:pk>", delete_adminquotation, name = "admin_deletequotation"),
    # path("DeleteQuotationAirlines/<int:air_id>/", delete_quotationAirlines, name="admin_deleteQuotationAirlines"),


    path("quotation-preview/<int:q_id>", preview_invoice ,name="q-preview"),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)