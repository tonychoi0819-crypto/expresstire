from django.conf import settings


def cart_context(request):
    from orders.models import Cart
    cart = Cart(request)
    return {
        'cart_item_count': cart.get_item_count(),
        'cart_total': cart.get_total(),
    }


def shop_info(request):
    return {
        'shop_name': settings.SHOP_NAME,
        'shop_phone': settings.SHOP_PHONE,
        'shop_whatsapp': settings.SHOP_WHATSAPP,
        'shop_email': settings.SHOP_EMAIL,
        'shop_address': settings.SHOP_ADDRESS,
        'shop_emergency': settings.SHOP_EMERGENCY,
        'shop_facebook': settings.SHOP_FACEBOOK,
        'shop_opening_hours': settings.SHOP_OPENING_HOURS,
    }


def payment_methods(request):
    return {'payment_methods': settings.PAYMENT_METHODS}
