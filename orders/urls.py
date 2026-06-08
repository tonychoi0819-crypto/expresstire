from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/process/', views.checkout_process, name='checkout_process'),
    path('order/<str:order_number>/', views.order_detail, name='order_detail'),
    path('order/<str:order_number>/payment/', views.order_payment, name='order_payment'),
    path('order/<str:order_number>/confirm/', views.order_confirm, name='order_confirm'),
]
