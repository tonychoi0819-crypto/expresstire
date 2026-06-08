from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('install/', views.install_booking, name='install_booking'),
    path('install/success/', views.install_success, name='install_success'),
    path('mobile/', views.mobile_booking, name='mobile_booking'),
    path('emergency/request/', views.emergency_request, name='emergency_request'),
]
