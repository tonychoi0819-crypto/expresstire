from django.shortcuts import render, get_object_or_404
from django.conf import settings

def cart_count(request):
    """Context processor to show cart count in all templates"""
    from .models import CartItem
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        session_key = request.session.session_key
        count = CartItem.objects.filter(session_key=session_key).count() if session_key else 0
    return {'cart_count': count}
