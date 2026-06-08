from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Min, Count
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from .models import Brand, Tyre, TyreVariant, Promotion
from orders.models import Cart, Lead
from django.conf import settings


def home(request):
    featured_tyres = Tyre.objects.filter(is_active=True, is_featured=True)[:8]
    new_arrivals = Tyre.objects.filter(is_active=True).order_by('-created')[:6]
    brands = Brand.objects.filter(is_active=True)[:12]
    promos = Promotion.objects.filter(
        is_active=True,
        start_date__lte=timezone.now(),
    ).filter(
        Q(end_date__gte=timezone.now()) | Q(end_date__isnull=True)
    )[:3]
    
    # Popular sizes - get actual variants for size links
    popular_sizes = TyreVariant.objects.filter(is_active=True).order_by('-tyre__view_count')[:8]

    context = {
        'featured_tyres': featured_tyres,
        'new_arrivals': new_arrivals,
        'brands': brands,
        'promos': promos,
        'popular_sizes': popular_sizes,
        'shop_name': settings.SHOP_NAME,
    }
    return render(request, 'tires/home.html', context)


def search(request):
    query = request.GET.get('q', '')
    width = request.GET.get('width')
    aspect = request.GET.get('aspect')
    diameter = request.GET.get('diameter')
    brand = request.GET.get('brand')
    tyre_type = request.GET.get('type')
    sort = request.GET.get('sort', 'price_low')

    variants = TyreVariant.objects.filter(is_active=True, tyre__is_active=True)

    if query:
        variants = variants.filter(
            Q(tyre__name__icontains=query) |
            Q(tyre__brand__name__icontains=query) |
            Q(size_display__icontains=query)
        )
    if width:
        variants = variants.filter(width=int(width))
    if aspect:
        variants = variants.filter(aspect=int(aspect))
    if diameter:
        variants = variants.filter(diameter=int(diameter))
    if brand:
        variants = variants.filter(tyre__brand__slug=brand)
    if tyre_type:
        variants = variants.filter(tyre__tyre_type=tyre_type)

    # Sort
    if sort == 'price_low':
        variants = variants.order_by('price')
    elif sort == 'price_high':
        variants = variants.order_by('-price')
    elif sort == 'newest':
        variants = variants.order_by('-tyre__created')
    elif sort == 'popular':
        variants = variants.order_by('-tyre__view_count')
    else:
        variants = variants.order_by('tyre__brand__name', 'price')

    # Stats
    total_variants = variants.count()
    price_range = variants.aggregate(min_price=Min('price'))

    context = {
        'variants': variants[:50],
        'total_variants': total_variants,
        'query': query,
        'min_price': price_range['min_price'],
        'brands': Brand.objects.filter(is_active=True),
    }
    return render(request, 'tires/search.html', context)


def tyre_detail(request, slug):
    tyre = get_object_or_404(Tyre, slug=slug, is_active=True)
    variants = tyre.variants.filter(is_active=True).order_by('price')
    
    # Track view
    tyre.view_count += 1
    tyre.save(update_fields=['view_count'])
    
    # Related tyres (same brand or type)
    related = Tyre.objects.filter(
        is_active=True
    ).filter(
        Q(brand=tyre.brand) | Q(tyre_type=tyre.tyre_type)
    ).exclude(id=tyre.id)[:6]
    
    # Selected variant
    selected_variant_id = request.GET.get('variant')
    selected_variant = None
    if selected_variant_id:
        selected_variant = TyreVariant.objects.filter(id=selected_variant_id, tyre=tyre).first()

    context = {
        'tyre': tyre,
        'variants': variants,
        'related_tyres': related,
        'selected_variant': selected_variant,
    }
    return render(request, 'tires/tyre_detail.html', context)


def brand_detail(request, slug):
    brand = get_object_or_404(Brand, slug=slug, is_active=True)
    tyres = brand.tyres.filter(is_active=True)
    return render(request, 'tires/brand_detail.html', {'brand': brand, 'tyres': tyres})


def brand_list(request):
    brands = Brand.objects.filter(is_active=True)
    return render(request, 'tires/brand_list.html', {'brands': brands})


def size_search(request, width, aspect, diameter):
    variants = TyreVariant.objects.filter(
        is_active=True,
        tyre__is_active=True,
        width=width,
        aspect=aspect,
        diameter=diameter
    ).order_by('price')
    
    return render(request, 'tires/search.html', {
        'variants': variants,
        'total_variants': variants.count(),
        'query': f'{width}/{aspect}R{diameter}',
        'is_size_search': True,
    })


# --- Cart ---

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'tires/cart.html', {'cart': cart})


def cart_add(request, variant_id):
    variant = get_object_or_404(TyreVariant, id=variant_id, is_active=True)
    cart = Cart(request)
    cart.add(variant)
    messages.success(request, f'{variant.tyre} {variant.size_display} added to cart')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'ok',
            'cart_count': cart.get_item_count(),
            'cart_total': cart.get_total(),
        })
    
    next_url = request.GET.get('next', 'tires:cart_detail')
    return redirect(next_url)


def cart_remove(request, variant_id):
    cart = Cart(request)
    cart.remove(variant_id)
    return redirect('tires:cart_detail')


def cart_update(request, variant_id):
    qty = int(request.POST.get('quantity', 1))
    cart = Cart(request)
    cart.update_quantity(variant_id, qty)
    next_url = request.POST.get('next', 'tires:cart_detail')
    return redirect(next_url)


# --- Coupon ---
def coupon_apply(request):
    code = request.POST.get('code', '').strip()
    if code:
        from orders.models import Coupon
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            if coupon.is_valid:
                request.session['coupon_id'] = coupon.id
                messages.success(request, f'Coupon "{code}" applied! {coupon.discount_value}{"%" if coupon.discount_type=="percent" else "HK$"} off')
            else:
                messages.error(request, 'This coupon has expired or reached maximum uses.')
        except Coupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')
    return redirect('tires:cart_detail')


# --- Lead ---
def enquiry_submit(request):
    if request.method == 'POST':
        Lead.objects.create(
            customer_name=request.POST.get('name', ''),
            customer_phone=request.POST.get('phone', ''),
            customer_email=request.POST.get('email', ''),
            tyre_interest=request.POST.get('tyre_interest', ''),
            size_interest=request.POST.get('size', ''),
            source='website',
            notes=request.POST.get('message', ''),
        )
        messages.success(request, 'Enquiry submitted! We will contact you within 1 hour.')
    return redirect('tires:home')


# --- Static pages ---
def about(request):
    return render(request, 'tires/about.html')


def install_info(request):
    from bookings.models import ShopLocation
    shops = ShopLocation.objects.filter(is_active=True)
    return render(request, 'tires/install_info.html', {'shops': shops})


def emergency_service(request):
    if request.method == 'POST':
        from bookings.models import EmergencyCall
        EmergencyCall.objects.create(
            caller_name=request.POST.get('name', ''),
            caller_phone=request.POST.get('phone', ''),
            location=request.POST.get('location', ''),
            vehicle_info=request.POST.get('vehicle', ''),
            service_type=request.POST.get('service_type', 'flat_tyre'),
            description=request.POST.get('description', ''),
        )
        messages.success(request, 'Emergency request received! Our team will contact you immediately.')
        return redirect('tires:emergency_service')
    return render(request, 'tires/emergency.html')



