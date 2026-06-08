from django.db import models
from django.utils import timezone


class InstallationBooking(models.Model):
    """Separate from order — for booking installation slots"""
    TIME_SLOTS = [
        ('08-10', '8:00-10:00 AM'),
        ('10-12', '10:00-12:00 PM'),
        ('12-14', '12:00-2:00 PM'),
        ('14-16', '2:00-4:00 PM'),
        ('16-18', '4:00-6:00 PM'),
        ('emergency', 'Emergency / 24hr Mobile'),
    ]
    BOOKING_TYPE = [
        ('shop', 'Shop Fitting'),
        ('mobile', 'Mobile Service'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=20, blank=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    
    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE, default='shop')
    shop_location = models.CharField(max_length=100, blank=True, help_text='For shop fitting')
    address = models.TextField(blank=True, help_text='For mobile service')
    
    # Date & time
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=10, choices=TIME_SLOTS)
    
    # Tyre info
    tyre_details = models.CharField(max_length=300, help_text='e.g. Michelin PS5 225/45R17 x4')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.customer_name} — {self.preferred_date} {self.get_preferred_time_slot_display()}'


class ShopLocation(models.Model):
    """Physical shop addresses"""
    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    opening_hours = models.CharField(max_length=100, default='Mon-Sat 8:00am-6:00pm')
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    map_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class EmergencyCall(models.Model):
    """24-hour emergency mobile tyre service requests"""
    SERVICE_TYPES = [
        ('flat_tyre', 'Flat Tyre'),
        ('battery', 'Dead Battery'),
        ('puncture', 'Puncture Repair'),
        ('tyre_change', 'Tyre Change'),
        ('jump_start', 'Jump Start'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('dispatched', 'Dispatched'),
        ('on_site', 'On Site'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    caller_name = models.CharField(max_length=100)
    caller_phone = models.CharField(max_length=20)
    location = models.TextField(help_text='Vehicle location / address')
    vehicle_info = models.CharField(max_length=100, blank=True, help_text='Car make/model/color')
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES, default='flat_tyre')
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    
    # GPS (if provided)
    lat = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Emergency Call'
        verbose_name_plural = 'Emergency Calls'
        ordering = ['-created']

    def __str__(self):
        return f'{self.caller_phone} — {self.get_service_type_display()} ({self.status})'
