from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Category, Product, Brand, CarMake, CarModel, CarYear, ProductFitment

def home(request):
    featured = Product.objects.filter(featured=True, available=True)[:8]
    categories = Category.objects.all()
    brands = Brand.objects.all()[:12]
    makes = CarMake.objects.all()[:20]
    return render(request, 'store/home.html', {
        'featured': featured,
        'categories': categories,
        'brands': brands,
        'makes': makes,
    })

def product_list(request):
    products = Product.objects.filter(available=True)
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    search = request.GET.get('q')
    product_type = request.GET.get('type')
    sort = request.GET.get('sort', '-created')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(brand__name__icontains=search)
        )
    if product_type:
        products = products.filter(product_type=product_type)

    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        '-created': '-created',
        'name': 'name',
    }
    products = products.order_by(sort_map.get(sort, '-created'))

    categories = Category.objects.all()
    brands = Brand.objects.all()
    current_category = categories.filter(slug=category_slug).first() if category_slug else None
    current_brand = brands.filter(slug=brand_slug).first() if brand_slug else None

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'current_category': current_category,
        'current_brand': current_brand,
        'current_type': product_type,
        'current_sort': sort,
        'search': search or '',
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    related = Product.objects.filter(
        category=product.category, available=True
    ).exclude(id=product.id)[:4]
    fitments = product.fitments.select_related('car_model__make').all()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
        'fitments': fitments,
    })

def fitment_selector(request):
    """Step-by-step car selector: Make -> Model -> Year -> Products"""
    makes = CarMake.objects.all().order_by('order', 'name')
    selected_make = None
    selected_model = None
    selected_year = None
    products = None
    models = None
    years = None

    make_slug = request.GET.get('make')
    model_slug = request.GET.get('model')
    year_id = request.GET.get('year')

    if make_slug:
        selected_make = get_object_or_404(CarMake, slug=make_slug)
        models = selected_make.models.all()
    if model_slug and selected_make:
        selected_model = get_object_or_404(CarModel, slug=model_slug, make=selected_make)
        years = selected_model.years.all()
    if year_id and selected_model:
        selected_year = get_object_or_404(CarYear, id=year_id, car_model=selected_model)
        product_ids = ProductFitment.objects.filter(
            car_model=selected_model,
            year_start__lte=selected_year.year,
        ).filter(
            Q(year_end__gte=selected_year.year) | Q(year_end__isnull=True)
        ).values_list('product_id', flat=True)
        products = Product.objects.filter(id__in=product_ids, available=True)

    return render(request, 'store/fitment_selector.html', {
        'makes': makes,
        'models': models,
        'years': years,
        'selected_make': selected_make,
        'selected_model': selected_model,
        'selected_year': selected_year,
        'products': products,
    })
