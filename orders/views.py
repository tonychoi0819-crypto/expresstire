import random
import string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import Order, OrderItem
from tires.models import TyreVariant


def generate_order_number():
    prefix = "ET"
    suffix = ''.join(random.choices(string.digits, k=6))
    order_num = f"{prefix}{suffix}"
    while Order.objects.filter(order_number=order_num).exists():
        suffix = ''.join(random.choices(string.digits, k=6))
        order_num = f"{prefix}{suffix}"
    return order_num


def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, "Your cart is empty")
        return redirect('tires:home')
    
    coupon = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        from orders.models import Coupon
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if not coupon.is_valid:
                coupon = None
                del request.session['coupon_id']
        except Coupon.DoesNotExist:
            pass
    
    discount = 0
    if coupon:
        discount = cart.get_total() - float(coupon.apply_discount(cart.get_total()))
    
    total = cart.get_total() - discount
    
    context = {
        'cart': cart,
        'coupon': coupon,
        'discount': discount,
        'total': total,
    }
    return render(request, 'orders/checkout.html', context)


def checkout_process(request):
    if request.method != 'POST':
        return redirect('tires:cart_detail')
    
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, "Your cart is empty")
        return redirect('tires:home')
    
    # Calculate total
    coupon = None
    discount = 0
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        from orders.models import Coupon
        try:
            coupon = Coupon.objects.get(id=coupon_id, is_active=True)
            if coupon.is_valid:
                discount = cart.get_total() - float(coupon.apply_discount(cart.get_total()))
                coupon.used_count += 1
                coupon.save()
        except Coupon.DoesNotExist:
            pass
    
    total = cart.get_total() - discount
    
    # Create order
    order = Order.objects.create(
        order_number=generate_order_number(),
        customer_name=request.POST.get('customer_name', ''),
        customer_phone=request.POST.get('customer_phone', ''),
        customer_email=request.POST.get('customer_email', ''),
        customer_address=request.POST.get('customer_address', ''),
        subtotal=cart.get_total(),
        discount=discount,
        coupon=coupon,
        total=total,
        install_type=request.POST.get('install_type', 'shop'),
        install_shop=request.POST.get('install_shop', ''),
        install_date=request.POST.get('install_date', None),
        install_time_slot=request.POST.get('install_time_slot', ''),
        notes=request.POST.get('notes', ''),
        payment_method=request.POST.get('payment_method', ''),
        source='website',
    )
    
    # Create order items & summary
    items_summary = []
    for item in cart:
        # Find variant
        variant_id = None
        for vid, vdata in cart.cart.items():
            if vdata['tyre_name'] == item['tyre_name'] and vdata['size'] == item['size']:
                variant_id = vid
                break
        
        parts = item['tyre_name'].rsplit(' ', 1)
        brand_name = parts[0] if len(parts) > 1 else ''
        tyre_name = parts[-1] if len(parts) > 1 else item['tyre_name']
        
        OrderItem.objects.create(
            order=order,
            tyre_name=tyre_name,
            brand_name=brand_name,
            size_display=item['size'],
            quantity=item['quantity'],
            unit_price=item['price'],
            total_price=item['total_price'],
        )
        items_summary.append(f"{item['tyre_name']} {item['size']} x{item['quantity']}")
    
    order.items_summary = ', '.join(items_summary)
    order.save()
    
    # Clear cart & coupon
    cart.clear()
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
    
    return redirect('orders:order_detail', order_number=order.order_number)


def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'orders/order_detail.html', {'order': order})


def order_payment(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    if request.method == 'POST':
        order.payment_ref = request.POST.get('payment_ref', '')
        order.payment_notes = request.POST.get('notes', '')
        if request.FILES.get('payment_proof'):
            order.payment_proof = request.FILES['payment_proof']
        order.status = 'paid'
        from django.utils import timezone
        order.paid_at = timezone.now()
        order.save()
        messages.success(request, 'Payment submitted! We will confirm within 30 minutes.')
        return redirect('orders:order_detail', order_number=order_number)
    return render(request, 'orders/order_payment.html', {'order': order})


def order_confirm(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    order.status = 'confirmed'
    order.save()
    messages.success(request, f'Order #{order_number} confirmed!')
    return redirect('orders:order_detail', order_number=order_number)
