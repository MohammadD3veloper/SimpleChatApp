from django.db import models
from django.contrib.auth.models import AbstractUser


def upload_image(instance, filename):
    return "images/%s/%s" % (instance, filename)


# Create your models here.
class Users(AbstractUser):
    profile_photo = models.ImageField(upload_to=upload_image)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    about = models.CharField(max_length=300)
    code = models.CharField(max_length=5)