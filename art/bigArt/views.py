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
from .filters import *
from django.core.mail import send_mail
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.utils import timezone


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
 

def about(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('about')
        else:
            messages.error(request, 'There was an error in your form submission. Please correct the errors below.')
    else:
        form = ContactForm()
    return render(request, 'bigArt/about.html', {'form': form})


def shop(request):
    products = Product.objects.all().order_by('id')
    product=ShopFilter(request.GET,queryset=products)
    categories = Category.objects.all() 
    products=product.qs
    context = {
        'products': products,
        'product': product,
        'categories': categories, 
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'bigArt/shop.html', context)

def shop(request):
    products = Product.objects.all().order_by('id')
    product=ShopFilter(request.GET,queryset=products)
    products=product.qs
    context = {
        'products': products,
        'product': product,
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'bigArt/shop.html', context)

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if created:
            cart.quantity = 1
        else:
            cart.quantity += 1
        cart.save()
        return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def remove_from_cart(request):
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'bigArt/cart.html', {'cart': cart})



@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.all()  # Query all items in the Cart model
    context = {
        'cart_items': cart_items
    }
    return render(request, 'bigArt/view_cart.html', context)


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
    order_details = request.session.get('order_details', {})
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] for item in cart)
    if request.method == 'POST':
        # Clear the cart
        request.session['cart'] = []
        return render(request, 'bigArt/order_confirmation.html', {'order_details': order_details, 'total_price': total_price})
    return render(request, 'bigArt/order_summary.html', {'order_details': order_details, 'cart': cart, 'total_price': total_price})


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


def paintings(request):
    paintings_category = Category.objects.get(name='Paintings')
    products_in_paintings_category = Product.objects.filter(category=paintings_category)
    painting_filter = ShopFilter(request.GET, queryset=products_in_paintings_category)
    filtered_paintings = painting_filter.qs
    
    return render(request, 'bigArt/painting.html', {'paintings': filtered_paintings, 'painting': painting_filter})

def drawing(request):
    drawings_category = Category.objects.get(name='Drawings')
    drawings = Product.objects.filter(category=drawings_category)
    drawing_filter = ShopFilter(request.GET, queryset=drawings)
    drawings = drawing_filter.qs
    return render(request, 'bigArt/drawings.html', {'drawings': drawings, 'drawing_filter': drawing_filter})


def ceramic(request):
    seramic_category = Category.objects.get(name='Ceramics')
    seramic = Product.objects.filter(category=seramic_category)
    seramic_filter = ShopFilter(request.GET, queryset=seramic)
    seramic = seramic_filter.qs
    return render(request, 'bigArt/ceramic.html', {'seramic': seramic, 'seramic_filter': seramic_filter})


def sculpture(request):
    sculpture_category = Category.objects.get(name='Sculpture')
    sculpture = Product.objects.filter(category=sculpture_category)
    sculpture_filter = ShopFilter(request.GET, queryset=sculpture)
    sculpture = sculpture_filter.qs
    return render(request, 'bigArt/sculptures.html', {'sculpture': sculpture, 'sculpture_filter': sculpture_filter})


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all()  # Get all reviews related to this product
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products
    }
    return render(request, 'bigArt/product_details.html', context)


def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user_name = request.user.username
            review.created_at = timezone.now()  # Set current timestamp
            review.save()
            messages.success(request, 'Your review has been submitted.')
            return redirect('product_detail', product_id=product_id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()

    return redirect('product_detail', product_id=product_id)  # Handle GET request gracefully


class MyPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'Accounts/password_reset_email.html'
    subject_template_name = 'Accounts/custom_password_reset_subject.txt'
    success_url = 'password_reset_done'  # Specify where to redirect after a successful reset request
  







