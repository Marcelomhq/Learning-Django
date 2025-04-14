from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser

# Create your models here.
class RegKey(models.Model):
    reg_key = models.CharField(max_length=300)
    used = models.BooleanField(default=False)
    def __str__(self):
        return self.reg_key

class User(AbstractUser):
    user_tag = models.AutoField(primary_key=True)
    reg_key = models.OneToOneField("RegKey",on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def reg_key_string(self):
        return self.reg_key.reg_key
    
    # @property
    # def password_string(self):
    #     return self.reg_key.reg_key

    def __str__(self):
        return self.username
    

# class User(AbstractBaseUser):
#     user_tag = models.AutoField(primary_key=True)
#     reg_key = models.OneToOneField("RegKey",on_delete=models.CASCADE)
#     username = models.CharField(max_length=100, unique=True)
#     # password = models.CharField(max_length=8)
#     created_at = models.DateTimeField(auto_now_add=True)

#     USERNAME_FIELD = "username"

#     def __str__(self):
#         return self.username
    
#     @property
#     def reg_key_string(self):
#         return self.reg_key.reg_key


class Task(models.Model):
    user_tag = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title