from django.db import models

# Create your models here.
class RegKey(models.Model):
    reg_key = models.CharField(max_length=300)
    def __str__(self):
        return self.reg_key

class User(models.Model):
    user_tag = models.AutoField(primary_key=True)
    reg_key = models.OneToOneField(RegKey,on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    user_tag = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title