from django.db import models
from django.conf import settings
from django.utils import timezone


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('percent', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    ]
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.PositiveIntegerField(default=100)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(default=timezone.now)
    valid_to = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-valid_from']

    def __str__(self):
        return self.code

    @property
    def is_valid(self):
        now = timezone.now()
        if self.valid_to:
            return self.is_active and self.used_count < self.max_uses and self.valid_from <= now <= self.valid_to
        return self.is_active and self.used_count < self.max_uses and self.valid_from <= now

    def apply_discount(self, total):
        if self.discount_type == 'percent':
            return total * (1 - self.discount_value / 100)
        return max(total - self.discount_value, 0)


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, variant, quantity=1):
        variant_id = str(variant.id)
        if variant_id not in self.cart:
            self.cart[variant_id] = {"quantity": 0, "price": str(variant.price), "size": variant.size_display, "tyre_name": str(variant.tyre)}
        self.cart[variant_id]["quantity"] += quantity
        self.save()

    def remove(self, variant_id):
        vid = str(variant_id)
        if vid in self.cart:
            del self.cart[vid]
            self.save()

    def update_quantity(self, variant_id, quantity):
        vid = str(variant_id)
        if vid in self.cart:
            if quantity > 0:
                self.cart[vid]["quantity"] = quantity
            else:
                del self.cart[vid]
            self.save()

    def __iter__(self):
        for item in self.cart.values():
            item["price"] = float(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total(self):
        return sum(float(item["price"]) * item["quantity"] for item in self.cart.values())

    def get_item_count(self):
        return len(self.cart)

    def clear(self):
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Payment"), ("paid", "Paid"), ("confirmed", "Confirmed"),
        ("installing", "Installing"), ("completed", "Completed"), ("cancelled", "Cancelled"), ("refunded", "Refunded"),
    ]
    PAYMENT_CHOICES = [
        ("fps", "FPS"), ("payme", "PayMe"), ("alipay", "Alipay HK"),
        ("credit_card", "Credit Card"), ("wechat", "WeChat Pay"), ("cash", "Cash"), ("bank_transfer", "Bank Transfer"),
    ]

    order_number = models.CharField(max_length=20, unique=True, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)
    customer_email = models.EmailField(blank=True)
    customer_address = models.TextField(blank=True)
    items_summary = models.TextField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    install_type = models.CharField(max_length=20, choices=[("shop", "Shop"), ("mobile_day", "Mobile Day"), ("mobile_night", "Mobile Night")], default="shop")
    install_shop = models.CharField(max_length=50, blank=True)
    install_date = models.DateField(blank=True, null=True)
    install_time_slot = models.CharField(max_length=30, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True)
    payment_ref = models.CharField(max_length=100, blank=True)
    payment_proof = models.ImageField(upload_to="payment_proofs/", blank=True, null=True)
    notes = models.TextField(blank=True)
    admin_notes = models.TextField(blank=True)
    source = models.CharField(max_length=20, default="website")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"#{self.order_number} - {self.customer_name} - ${self.total}"

    @property
    def tyre_count(self):
        if not self.items_summary:
            return 0
        import re
        return sum(int(m) for m in re.findall(r"x\s*(\d+)", self.items_summary))


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    tyre_name = models.CharField(max_length=200)
    brand_name = models.CharField(max_length=100)
    size_display = models.CharField(max_length=30)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.tyre_name} {self.size_display} x{self.quantity}"


class Lead(models.Model):
    SOURCE_CHOICES = [("website", "Website"), ("whatsapp", "WhatsApp"), ("phone", "Phone"), ("facebook", "Facebook"), ("google", "Google Ads"), ("referral", "Referral")]
    STATUS_CHOICES = [("new", "New"), ("contacted", "Contacted"), ("quoted", "Quoted"), ("converted", "Converted"), ("lost", "Lost")]
    customer_name = models.CharField(max_length=100, blank=True)
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_email = models.EmailField(blank=True)
    tyre_interest = models.CharField(max_length=200, blank=True)
    size_interest = models.CharField(max_length=30, blank=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default="website")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lead"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.customer_phone or self.customer_email} - {self.tyre_interest}"
