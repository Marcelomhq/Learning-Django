from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from .models import RegKey

class RegisterForm(forms.Form):
    username = forms.EmailField(
        label="Username (Email)", 
        validators=[EmailValidator()], 
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )

    password = forms.CharField(
        label="Password (6-8 characters)",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
        min_length=6,
        max_length=8
    )

    reg_key = forms.CharField(
        label="Register Key",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter Register Key"})
    )

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("This email is already registered!")
        return username

    def clean_reg_key(self):
        reg_key = self.cleaned_data["reg_key"]
        if not RegKey.objects.filter(reg_key=reg_key).exists():
            raise ValidationError("Invalid Registration Key!")
        return reg_key
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6 or len(password) > 8:
            raise ValidationError("Password must be 6-8 characters!")
        return password
