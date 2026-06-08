from django.contrib import admin
from tires.models import Brand, Tyre, TyreVariant, Promotion
from orders.models import Order, OrderItem, Coupon, Lead
from bookings.models import InstallationBooking, ShopLocation, EmergencyCall


# Tires
class TyreVariantInline(admin.TabularInline):
    model = TyreVariant
    extra = 1


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active', 'tyres_count']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active']

    def tyres_count(self, obj):
        return obj.tyres.count()


@admin.register(Tyre)
class TyreAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'tyre_type', 'is_featured', 'is_active', 'lowest_price', 'variant_count']
    list_filter = ['brand', 'tyre_type', 'is_featured', 'is_active']
    search_fields = ['name', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [TyreVariantInline]


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_type', 'discount_value', 'is_active', 'is_current']
    list_filter = ['is_active', 'discount_type']


# Orders
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['tyre_name', 'brand_name', 'size_display', 'quantity', 'unit_price', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_phone', 'total', 'status', 'payment_method', 'source', 'created']
    list_filter = ['status', 'payment_method', 'source', 'install_type']
    search_fields = ['order_number', 'customer_name', 'customer_phone']
    readonly_fields = ['order_number', 'created', 'updated']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Order Info', {'fields': ('order_number', 'status', 'source', 'created', 'updated')}),
        ('Customer', {'fields': ('customer_name', 'customer_phone', 'customer_email', 'customer_address')}),
        ('Items & Pricing', {'fields': ('items_summary', 'subtotal', 'discount', 'coupon', 'total')}),
        ('Installation', {'fields': ('install_type', 'install_shop', 'install_date', 'install_time_slot', 'install_notes')}),
        ('Payment', {'fields': ('payment_method', 'payment_ref', 'payment_proof', 'payment_notes', 'paid_at')}),
        ('Notes', {'fields': ('notes', 'admin_notes')}),
    )


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'used_count', 'max_uses', 'is_valid', 'is_active']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'tyre_interest', 'size_interest', 'status', 'source', 'created']
    list_filter = ['status', 'source']
    search_fields = ['customer_name', 'customer_phone', 'customer_email']


# Bookings
@admin.register(InstallationBooking)
class InstallBookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'booking_type', 'preferred_date', 'preferred_time_slot', 'status', 'created']
    list_filter = ['booking_type', 'status', 'preferred_date']


@admin.register(ShopLocation)
class ShopLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_main', 'is_active']


@admin.register(EmergencyCall)
class EmergencyCallAdmin(admin.ModelAdmin):
    list_display = ['caller_name', 'caller_phone', 'service_type', 'location', 'status', 'created']
    list_filter = ['service_type', 'status']
