from django.contrib import admin
from .models import (
    CarMake, CarModel, CarYear, Brand, Category, Product, ProductFitment
)

class CarYearInline(admin.TabularInline):
    model = CarYear
    extra = 1

class ProductFitmentInline(admin.TabularInline):
    model = ProductFitment
    extra = 1

@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    inlines = []

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'make', 'slug']
    list_filter = ['make']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CarYearInline]

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'brand', 'product_type', 'price', 'discount_price', 'stock', 'available', 'featured']
    list_filter = ['category', 'brand', 'product_type', 'available', 'featured']
    list_editable = ['price', 'discount_price', 'stock', 'available', 'featured']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductFitmentInline]
