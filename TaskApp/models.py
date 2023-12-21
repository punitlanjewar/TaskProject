from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile')
    user_address = models.TextField()
    user_city = models.CharField(max_length=100)
    user_lane = models.CharField(max_length=100)
    user_state = models.CharField(max_length=100)
    user_pincode = models.IntegerField()

class BlogCategory(models.Model):
    category_name = models.CharField(max_length=200)


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blogimage')
    category = models.ForeignKey(BlogCategory,  on_delete=models.CASCADE)
    summary = models.TextField()
    content = models.TextField()
    draft = models.BooleanField(default=False)

