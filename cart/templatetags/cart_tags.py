from django import template
from cart.models import CartItem

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_count(context):
    request = context['request']
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user).count()
    session_key = request.session.session_key
    if session_key:
        return CartItem.objects.filter(session_key=session_key).count()
    return 0
