from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),  
    path('sign/', views.signup, name='signup_html'), 
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about, name='about'),
]
