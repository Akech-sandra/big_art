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
# import pagination stuff
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

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
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Exception:
        cart = None
        cart_items = []

    products = Product.objects.all()
  
    p=Paginator(Product.objects.all(),3)
    page_number = request.GET.get('page')
    pages_obj = p.get_page(page_number)
    product = ShopFilter(request.GET, queryset=products)
    categories = Category.objects.all() 
    products = product.qs
    
    if request.user.is_authenticated:
        user = request.user
        session_key = None
    else:
        user = None
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
    
    # Create a PageView entry if it doesn't already exist for this session or user
    if not PageView.objects.filter(user=user, session_key=session_key).exists():
        PageView.objects.create(user=user, session_key=session_key)

    # Get the total number of page views and unique viewers
    total_views = PageView.objects.count()
    unique_viewers = PageView.objects.values('user', 'session_key').distinct().count()

    context = {
        'cart': cart_items,
        'pages_obj': pages_obj,
        'products': products,
        'product': product,
        'total_views': total_views,
        'unique_viewers': unique_viewers,
        'categories': categories, 
        'user_is_authenticated': request.user.is_authenticated
    }
    return render(request, 'bigArt/shop.html', context)

# def add_to_cart(request, product_id):
#     if request.method == 'POST':
#         product = Product.objects.get(id=product_id)
#         cart, created = Cart.objects.get_or_create(user=request.user)
#         CartItem.objects.create(cart=cart,product=product, unit_price =product.unit_price,quantity=1,total_price=product.unit_price)
#         cart.save()
#         res =  {'name': product.product_name,'unit_price': product.unit_price,  'quantity': 1, 'total_price': product.unit_price }
#         return JsonResponse({'status': 'success', 'message': 'Product added to cart','data': res})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.create(cart=cart,product=product, unit_price =product.unit_price,quantity=1,total_price=product.unit_price)
        cart.save()
        res =  {'name': product.product_name,'unit_price': product.unit_price,  'quantity': 1, 'total_price': product.unit_price }
        return JsonResponse({'status': 'success', 'message': 'Product added to cart','data': res})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    cart_data = [{'product': {'product_name': item.product.product_name, 'unit_price': item.product.unit_price}, 'quantity': item.quantity} for item in cart_items]
    return JsonResponse({'cart': cart_data})@login_required
# def cart_detail(request):
#     cart = get_object_or_404(Cart, user=request.user)
#     return render(request, 'bigArt/cart.html', {'cart': cart})
@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'bigArt/cart.html', {'cart_items': cart_items})



# def remove_from_cart(request, product_id):
#     if request.method == 'POST':
#         try:
#             cart_item = Cart.objects.get(user=request.user, product_id=product_id)
#             cart_item.delete()
#             return JsonResponse({'status': 'success', 'message': 'Item removed from cart.'})
#         except Cart.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Item not found in cart.'})
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            cart_item = CartItem.objects.get(product_id=product_id, user=request.user)
            cart_item.delete()
            return JsonResponse({'status': 'success'}, status=200)
        except CartItem.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item does not exist in cart'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@login_required
def view_cart(request):
    cart_items = Cart.objects.all()  # Query all items in the Cart model
    context = {
        'cart_items': cart_items
    }
    return render(request, 'bigArt/view_cart.html', context)


@login_required
def checkout(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Exception:
        cart = None
        cart_items = []
    total_price = sum(item.total_price for item in cart_items)
    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        order = Order.objects.create(user=request.user, shipping_address=shipping_address, payment_method=payment_method, total_price=total_price, date_ordered=timezone.now())
        for item in cart_items:
            order.items.create(product=item.product, quantity=item.quantity, unit_price=item.unit_price, total_price=item.total_price)
        cart_items.delete()
        cart.delete()
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'bigArt/checkout.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_details = order.items.all()
    total_price = order.total_price
    user = order.user

    if request.method == 'POST':
        if order.status == 'Pending':
            # Reduce the product quantities
            for item in order_details:
                product = item.product
                if product.quantity >= item.quantity:
                    product.quantity -= item.quantity
                    product.save()
                else:
                    return HttpResponse(f"Insufficient product quantity for {product.product_name}")

            # Update order status
            order.status = 'Confirmed'
            order.save()

            # Email content with user details
            email_subject = 'Order Confirmed'
            email_body = f'''
            Order {order.id} has been confirmed.
            User Details:
            Username: {user.username}
            Email: {user.email}
            First Name: {user.first_name}
            Last Name: {user.last_name}
            Shipping Address: {order.shipping_address}
            Total Price: {order.total_price}
            '''

            # Send email to admin
            send_mail(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,
                ['bigartug24@gmail.com'], 
                fail_silently=False,
            )

            return HttpResponseRedirect(reverse('order_confirmation', args=[order.id]))

        return HttpResponse("Order is already confirmed.")

    return render(request, 'bigArt/order_confirm.html', {'order_details': order_details, 'total_price': total_price})
def cancel_order(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()
    cart.delete()
    messages.success(request, 'Your order has been canceled.')
    return redirect('shop')

def gallery(request):
    return render(request, 'bigArt/gallery.html')

def contact(request):
    return render(request, 'bigArt/contact.html')

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review')
    else:
        form = ReviewForm()
    return render(request, 'bigArt/review.html', {'form': form})


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
  







