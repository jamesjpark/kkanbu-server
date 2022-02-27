from this import d
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
import rest_framework.authtoken.models
from django.contrib.postgres.fields import ArrayField

from django.conf import settings


# Create your models here.

class Age_group(models.Model):
    AG10 = '10s'
    AG20 = '20s'
    AG30 = '30s'
    AG40 = '40s'
    AG50 = '50s'

    AGE_GROUP_CHOICES = (
        (AG10, '10s'),
        (AG20, '20s'),
        (AG30, '30s'),
        (AG40, '40s'),
        (AG50, '50s'),
    )

class Gender(models.Model):
    MALE = 'male'
    FEMALE = 'female'

    GENDER_CHOICES = (
        (MALE, 'male'),
        (FEMALE, 'female')
    )



class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    login_type = models.CharField(max_length=30)
    name = models.CharField( max_length=5)
    age_group = ArrayField(
        models.CharField(choices = Age_group.AGE_GROUP_CHOICES, max_length=5),
        size = 5,
        default = list,
        blank = True
    )
    city= ArrayField(
        models.CharField(max_length=10),
        size = 3,
        default = list,
        blank = True
    )
    gender = models.CharField(choices = Gender.GENDER_CHOICES, max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
