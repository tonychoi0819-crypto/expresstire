from django.contrib import admin
from .models import CartItem

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'session_key', 'quantity', 'added_at']
    list_filter = ['added_at']
