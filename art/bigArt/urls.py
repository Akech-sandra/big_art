from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import MyPasswordResetView


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('sign/', views.signup, name='signup'), 
    path('logout/', views.logout_view, name='logout'),
    
    path('about/', views.about, name='about'),
    path('shop/', views.shop, name='shop'),
    
    path('paintings/', views.paintings, name='paintings'),
    path('sculptures/', views.sculpture, name='sculptures'),
    path('drawings/', views.drawing, name='drawings'),
    path('ceramic/', views.ceramic, name='ceramic'),
    
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
  
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    
   path('checkout/', views.checkout, name='checkout'),
    
    # reset password(urls)
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='Accounts/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="Accounts/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='Accounts/password_reset_complete.html') ,name='password_reset_complete'),

    



] 
