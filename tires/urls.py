from django.urls import path
from . import views

app_name = 'tires'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('tyre/<slug:slug>/', views.tyre_detail, name='tyre_detail'),
    path('brand/<slug:slug>/', views.brand_detail, name='brand_detail'),
    path('brands/', views.brand_list, name='brand_list'),
    path('size/<int:width>/<int:aspect>/<int:diameter>/', views.size_search, name='size_search'),
    
    # Cart
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:variant_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:variant_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:variant_id>/', views.cart_update, name='cart_update'),
    
    # Coupon
    path('coupon/apply/', views.coupon_apply, name='coupon_apply'),
    
    # Lead capture
    path('enquiry/', views.enquiry_submit, name='enquiry'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('install/', views.install_info, name='install_info'),
    path('emergency/', views.emergency_service, name='emergency_service'),
]
