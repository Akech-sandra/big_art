from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

# Create your models here.

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Create and save a user with the given email and password.
        if not email:
            raise ValueError('The Email field is required')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set the password using Django's hashing function
        self.save(user, commit=True)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create a superuser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if password is None:
            raise ValueError('Password is required for superusers')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100) 
    address = models.CharField(max_length=100) 
    gender = models.CharField(max_length=10)  

    USERNAME_FIELD = 'email'  # Set the field used for authentication to email
    REQUIRED_FIELDS = []  # No additional fields are required for authentication

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.product_name

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    

    
class Painting(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    short_description = models.TextField(default="No description available")
    description = models.TextField()
    image = models.ImageField(upload_to='paintings/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title    