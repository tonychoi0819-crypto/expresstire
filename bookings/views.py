from django.shortcuts import render, redirect
from django.contrib import messages
from .models import InstallationBooking, ShopLocation, EmergencyCall


def install_booking(request):
    shops = ShopLocation.objects.filter(is_active=True)
    if request.method == 'POST':
        InstallationBooking.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_phone=request.POST.get('phone', ''),
            customer_email=request.POST.get('email', ''),
            booking_type='shop',
            shop_location=request.POST.get('shop', ''),
            preferred_date=request.POST.get('date', ''),
            preferred_time_slot=request.POST.get('time_slot', ''),
            tyre_details=request.POST.get('tyre_details', ''),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Installation booking submitted! We will confirm via phone.')
        return redirect('bookings:install_success')
    return render(request, 'bookings/install_booking.html', {'shops': shops})


def install_success(request):
    return render(request, 'bookings/install_success.html')


def mobile_booking(request):
    if request.method == 'POST':
        InstallationBooking.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_phone=request.POST.get('phone', ''),
            customer_email=request.POST.get('email', ''),
            booking_type='mobile',
            address=request.POST.get('address', ''),
            preferred_date=request.POST.get('date', ''),
            preferred_time_slot=request.POST.get('time_slot', ''),
            tyre_details=request.POST.get('tyre_details', ''),
            notes=request.POST.get('notes', ''),
        )
        messages.success(request, 'Mobile fitting request submitted! We will confirm via phone.')
        return redirect('bookings:install_success')
    return render(request, 'bookings/mobile_booking.html')


def emergency_request(request):
    if request.method == 'POST':
        EmergencyCall.objects.create(
            caller_name=request.POST.get('name', ''),
            caller_phone=request.POST.get('phone', ''),
            location=request.POST.get('location', ''),
            vehicle_info=request.POST.get('vehicle', ''),
            service_type=request.POST.get('service_type', 'flat_tyre'),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Emergency request received! Our team will contact you immediately.')
        return redirect('tires:emergency_service')
    return render(request, 'bookings/emergency_form.html')
