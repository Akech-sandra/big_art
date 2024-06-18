from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.index, name='index'),
    # path('login/', auth_views.LoginView.as_view(template_name='bigArt/login.html'), name='login'),
    # path('login/', views.login_view, name='login'),   
    path('login/', views.user_login, name='login'),
    path('sign/', views.signup, name='signup_html'), 
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('remove_from_cart/<int:index>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('paintings/', views.paintings_view, name='paintings'),

    



] 
