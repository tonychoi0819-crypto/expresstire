from django.db import models
from django.urls import reverse

class CarMake(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='car_logos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Car Make'
        verbose_name_plural = 'Car Makes'

    def __str__(self):
        return self.name

class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    class Meta:
        ordering = ['name']
        unique_together = ('make', 'slug')
        verbose_name = 'Car Model'
        verbose_name_plural = 'Car Models'

    def __str__(self):
        return f'{self.make.name} {self.name}'

class CarYear(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='years')
    year = models.PositiveIntegerField()

    class Meta:
        ordering = ['-year']
        unique_together = ('car_model', 'year')
        verbose_name = 'Model Year'
        verbose_name_plural = 'Model Years'

    def __str__(self):
        return f'{self.car_model} {self.year}'

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_list') + f'?category={self.slug}'

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('tyre', 'Tyre'),
        ('rim', 'Rim / Wheel'),
        ('package', 'Tyre + Rim Package'),
        ('accessory', 'Accessory'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='tyre')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Fitment fields (for tyres)
    tyre_width = models.CharField(max_length=10, blank=True, help_text='e.g. 225')
    tyre_aspect = models.CharField(max_length=10, blank=True, help_text='e.g. 45')
    tyre_diameter = models.CharField(max_length=10, blank=True, help_text='e.g. 17')
    tyre_load_index = models.CharField(max_length=10, blank=True)
    tyre_speed_rating = models.CharField(max_length=10, blank=True)

    # Fitment fields (for rims)
    rim_diameter = models.CharField(max_length=10, blank=True, help_text='e.g. 17')
    rim_width = models.CharField(max_length=10, blank=True, help_text='e.g. 8.0')
    rim_pcd = models.CharField(max_length=20, blank=True, help_text='e.g. 5x114.3')
    rim_offset = models.CharField(max_length=10, blank=True, help_text='e.g. ET45')
    rim_center_bore = models.CharField(max_length=10, blank=True, help_text='e.g. 73.1')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])

    @property
    def get_price(self):
        if self.discount_price:
            return self.discount_price
        return self.price

    @property
    def get_discount_percent(self):
        if self.discount_price and self.price > 0:
            return int((1 - self.discount_price / self.price) * 100)
        return 0

    @property
    def tyre_size_display(self):
        if self.tyre_width and self.tyre_aspect and self.tyre_diameter:
            return f'{self.tyre_width}/{self.tyre_aspect}R{self.tyre_diameter}'
        return ''

    @property
    def rim_size_display(self):
        if self.rim_diameter and self.rim_width:
            return f'{self.rim_width}x{self.rim_diameter}"'
        return ''

class ProductFitment(models.Model):
    """Links a product to compatible car model+years"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fitments')
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year_start = models.PositiveIntegerField()
    year_end = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        verbose_name = 'Product Fitment'
        verbose_name_plural = 'Product Fitments'

    def __str__(self):
        year_range = f'{self.year_start}'
        if self.year_end and self.year_end != self.year_start:
            year_range += f'-{self.year_end}'
        return f'{self.product.name} → {self.car_model} ({year_range})'
