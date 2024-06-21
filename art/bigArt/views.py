from django.shortcuts import render, get_object_or_404, redirect 
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from.models import *
from.forms import *
from django.contrib.auth.decorators import login_required
from .forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import CustomUser
from django.db import IntegrityError
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, 'bigArt/index.html')



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            phone_number = form.cleaned_data.get('phone_number')
            physical_address = form.cleaned_data.get('physical_address')
            gender = form.cleaned_data.get('gender')
            
            if password1 == password2:
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(username=email, email=email, first_name=first_name, last_name=last_name)
                    user.set_password(password1)
                    user.save()
                    return redirect('login')
            else:
                messages.error(request, 'Passwords do not match')
                return redirect('signup')
    else:
        form = SignUpForm()
    return render(request, 'bigArt/sign.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password1']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('shop')
        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'bigArt/login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')
        else:
            messages.error(request, 'There was an error in your form submission. Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'bigArt/contact.html', {'form': form})  

def about(request):
    return render(request, 'bigArt/about.html')

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'bigArt/shop.html', context)

def paint(request):
    return render(request, 'bigArt/painting.html')


def checkout(request):
    cart = request.session.get('cart', [])
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the order
            request.session['order_details'] = form.cleaned_data
            return redirect('order_confirmation')
    else:
        form = CheckoutForm()
    total_price = sum(item['price'] for item in cart)
    return render(request, 'bigArt/checkout.html', {'cart': cart, 'total_price': total_price, 'form': form})

def order_confirmation(request):
    order_details = request.session.get('order_details', {})
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    if request.method == 'POST':
        # Clear the cart
        request.session['cart'] = []
        return render(request, 'bigArt/order_confirmation.html', {'order_details': order_details, 'total_price': total_price})
    return render(request, 'bigArt/order_summary.html', {'order_details': order_details, 'cart': cart, 'total_price': total_price})


def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    if 0 <= index < len(cart):
        del cart[index]
        request.session['cart'] = cart
    return redirect('view_cart')



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'bigArt/view_cart.html', {'cart_items': cart_items, 'total_price': total_price})



@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total_price=sum(item.product.price * item.quantity for item in cart_items))
            cart_items.delete()  # Clear the cart after creating the order
            return redirect('order_confirmation')
    else:
        form = CheckoutForm()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'bigArt/checkout.html', {'cart_items': cart_items, 'total_price': total_price, 'form': form})

@login_required
def order_confirmation(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bigArt/order_confirmation.html', {'orders': orders})

def paintings_view(request):
    paintings = Painting.objects.all()
    return render(request, 'bigArt/paintings.html', {'paintings': paintings})







