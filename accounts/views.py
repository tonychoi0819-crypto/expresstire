from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from cart.models import CartItem

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Merge session cart into user cart
            session_key = request.session.session_key
            if session_key:
                session_items = CartItem.objects.filter(session_key=session_key)
                for item in session_items:
                    existing = CartItem.objects.filter(user=user, product=item.product).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.user = user
                        item.session_key = None
                        item.save()
                session_items.delete()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Merge session cart
            session_key = request.session.session_key
            if session_key:
                for item in CartItem.objects.filter(session_key=session_key):
                    existing = CartItem.objects.filter(user=user, product=item.product).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.user = user
                        item.session_key = None
                        item.save()
            next_url = request.GET.get('next', 'store:home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('store:home')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
