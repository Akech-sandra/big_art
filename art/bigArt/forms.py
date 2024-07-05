from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
import re
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone_number = forms.CharField(required=True, max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    physical_address = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Physical Address'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    gender = forms.ChoiceField(
        choices=[('', 'Gender'), ('Male', 'Male'), ('Female', 'Female')],
        required=True,
        widget=forms.Select()
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'physical_address', 'password1', 'password2', 'gender']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already in use")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?1?\d{9,15}$', phone_number):
            raise forms.ValidationError("Phone number is not valid")
        return phone_number

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        validate_password(password)
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords don\'t match.')
        return password2

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.password = make_password(self.cleaned_data['password1'])  # Hash password
        if commit:
            user.save()
        return user



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 55}),
        }
        
class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea)
    payment_method = forms.ChoiceField(choices=[('card', 'Credit Card'), ('paypal', 'PayPal')])

class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = '__all__'
        

class PaintingForm(forms.Form):
    class Meta:
        model = Painting
        fields = '__all__'       