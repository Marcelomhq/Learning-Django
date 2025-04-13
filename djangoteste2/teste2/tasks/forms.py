from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from .models import RegKey,User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )

    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )

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

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name").capitalize()
        if not first_name.isalpha():
            raise ValidationError("First name must contain only letters, no numbers, symbols or spaces")
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get("last_name").capitalize()
        if not last_name.isalpha():
            raise ValidationError("Last name must contain only letters, no numbers, symbols or spaces")
        return last_name

    def clean_username(self):
        username = self.cleaned_data.get("username").lower()        
        if User.objects.filter(username=username).exists():
            raise ValidationError("This email is already registered!")
        return username

    def clean_reg_key(self):
        reg_key = self.cleaned_data.get("reg_key")
        reg_key_obj = RegKey.objects.filter(reg_key=reg_key, used = False).first()
        if not reg_key_obj:
        # (not reg_key_obj.exists()) or (RegKey.objects.get(reg_key=reg_key).used != False) :
            raise ValidationError("Invalid or already used Registration Key!")
        self.cleaned_data["reg_key_obj"] = reg_key_obj
        return reg_key
    
    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6 or len(password) > 8:
            raise ValidationError("Password must be 6-8 characters!")
        return password

class TheLoginForm(forms.Form):
    username = forms.EmailField(
        label="Username (Email)", 
        # validators=[EmailValidator()], 
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )

    password = forms.CharField(
        label="Password (6-8 characters)",
        widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}),
        min_length=6,
        max_length=8
    )

    
    

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if not username:
            raise ValidationError("Username must be a valid email")
        
        user = authenticate(username=username.lower(),password=password)
       
        if not user:
            self.add_error("username","Username can't be found or Password is incorrect.")
        else:
            cleaned_data["user"] = user
        return cleaned_data

class ResetPasswordForm(forms.Form):
    first_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )

    last_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your first name"})
    )

    username = forms.EmailField(
        label="Username (Email)", 
        validators=[EmailValidator()], 
        widget=forms.EmailInput(attrs={"placeholder": "Enter your email"})
    )

#old login form        
        # if not User.objects.filter(username=username).exists():
        #     self.add_error("username","Username can't be found.")
        # else:

        #     user = User.objects.get(username=username)

        #     if not check_password(password,user.password):
        #         self.add_error("password","Password incorrect.")
            
        #     return cleaned_data
    
    # def good_username(self):
    #     username = self.cleaned_data["username"]
    #     if not User.objects.filter(username=username).exists():
    #         print("username couldnt be found")
    #         raise ValidationError("Username can't be found, check if your email is correct.")
    #     print("username was found")  
    #     return username

    # def good_password(self,username):
    #     password = self.cleaned_data["password"]
    #     username_obj = User.objects.get(username=username)
    #     password_obj = username_obj.password
    #     if not password == password_obj:
    #         print("pass couldnt be found")
    #         raise ValidationError("Password incorrectly, try again.")
    #     print("pass was be found")
    #     return password_obj

