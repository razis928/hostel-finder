from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('check_availability/', views.check_availability, name='check_availability'),
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('terms_conditions', views.terms_conditions, name="terms_conditions"),
    path('profile', views.profile, name="profile"),
    path('all_hostels', views.all_hostels, name="all_hostels"),
    path('hostels/', views.hostel_list, name='hostel_list'),
    path('hostel/<int:pk>/', views.hostel_detail, name='hostel_detail'),
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('contact', views.contact, name="contact"),
    path('customer-register', views.customer_register, name="customer_register"),
    path('hostel-owner-register', views.hostel_owner_register, name="hostel_owner_register"),
    path('login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name="user_logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)