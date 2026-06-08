from django.db import models
from django.conf import settings

class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    car_info = models.CharField(max_length=200, blank=True, help_text='e.g. Honda Civic 2020')

    def __str__(self):
        return f'{self.user.username} Profile'
