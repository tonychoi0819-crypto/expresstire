from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from store.models import Product
from .models import CartItem

def get_cart(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return CartItem.objects.filter(session_key=session_key)

def cart_view(request):
    items = get_cart(request)
    subtotal = sum(item.total_price for item in items)
    from django.conf import settings
    free_threshold = getattr(settings, 'FREE_SHIPPING_THRESHOLD', 2000)
    shipping = 0 if subtotal >= free_threshold else 200
    total = subtotal + shipping
    return render(request, 'cart/cart.html', {
        'items': items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'free_threshold': free_threshold,
    })

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    qty = int(request.POST.get('quantity', 1))

    if request.user.is_authenticated:
        item, created = CartItem.objects.get_or_create(
            user=request.user, product=product,
            defaults={'quantity': qty}
        )
        if not created:
            item.quantity += qty
            item.save()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        item, created = CartItem.objects.get_or_create(
            session_key=session_key, product=product,
            defaults={'quantity': qty}
        )
        if not created:
            item.quantity += qty
            item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        count = get_cart(request).count()
        return JsonResponse({'status': 'ok', 'cart_count': count})
    return redirect('cart:cart_view')

def cart_update(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        item.quantity = qty
        item.save()
    else:
        item.delete()
    return redirect('cart:cart_view')

def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart:cart_view')
