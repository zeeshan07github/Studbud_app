from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location=settings.MEDIA_ROOT)
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Topic(models.Model):
    # host =
    name = models.CharField( max_length=50)
    def __str__(self):
        return self.name

class room(models.Model):
    host =models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic ,  on_delete=models.SET_NULL , null=True)
    name = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, related_name='participants' , blank=True)
    description = models.CharField( max_length=250)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.name

class message(models.Model):
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    room = models.ForeignKey(room ,  on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-updated' , '-created']
    def __str__(self):
        return self.body[0:20]
    