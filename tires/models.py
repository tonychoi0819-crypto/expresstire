from django.db import models
from django.urls import reverse
from django.utils import timezone


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, null=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tires:brand_detail', args=[self.slug])


class Tyre(models.Model):
    TYRE_TYPE_CHOICES = [
        ('performance', 'Performance'),
        ('touring', 'Touring / Comfort'),
        ('suv', 'SUV / 4x4'),
        ('light_truck', 'Light Truck / Van'),
        ('ev', 'Electric Vehicle'),
    ]
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='tyres')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='tyres/', blank=True, null=True)
    description = models.TextField(blank=True)
    features = models.TextField(blank=True, help_text='Key selling points, one per line')
    tyre_type = models.CharField(max_length=20, choices=TYRE_TYPE_CHOICES, default='performance')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    view_count = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['brand__name', 'name']

    def __str__(self):
        return f'{self.brand.name} {self.name}'

    def get_absolute_url(self):
        return reverse('tires:tyre_detail', args=[self.slug])

    @property
    def lowest_price(self):
        prices = self.variants.filter(is_active=True).values_list('price', flat=True)
        if prices:
            return min(prices)
        return None

    @property
    def variant_count(self):
        return self.variants.filter(is_active=True).count()


class TyreVariant(models.Model):
    tyre = models.ForeignKey(Tyre, on_delete=models.CASCADE, related_name='variants')
    size_display = models.CharField(max_length=30, help_text='e.g. 225/45R17')
    width = models.PositiveIntegerField()
    aspect = models.PositiveIntegerField()
    diameter = models.PositiveIntegerField()
    load_index = models.CharField(max_length=10, blank=True)
    speed_rating = models.CharField(max_length=5, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='HKD per tyre, includes installation & balancing')
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='For showing discounts')
    in_stock = models.BooleanField(default=True)
    stock_qty = models.PositiveIntegerField(default=4, help_text='Number of tyres available')
    is_active = models.BooleanField(default=True)
    notes = models.CharField(max_length=200, blank=True, help_text='e.g. "EV only", "SUV fitment"')

    class Meta:
        unique_together = ('tyre', 'size_display')
        ordering = ['width', 'aspect', 'diameter']

    def __str__(self):
        return f'{self.tyre} {self.size_display}'

    def get_absolute_url(self):
        return reverse('tires:tyre_detail', args=[self.tyre.slug]) + f'?variant={self.id}'

    @property
    def discount_pct(self):
        if self.original_price and self.original_price > self.price:
            return int((1 - self.price / self.original_price) * 100)
        return 0


class Promotion(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Percentage Off'),
        ('fixed', 'Fixed Amount Off'),
        ('bundle', 'Bundle Deal'),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percent')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_qty = models.PositiveIntegerField(default=1, help_text='Minimum tyre qty to qualify')
    code = models.CharField(max_length=50, blank=True, help_text='Discount code (optional)')
    image = models.ImageField(upload_to='promos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created']

    def __str__(self):
        return self.title

    @property
    def is_current(self):
        now = timezone.now()
        if self.end_date:
            return self.is_active and self.start_date <= now <= self.end_date
        return self.is_active and self.start_date <= now
