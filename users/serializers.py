from urllib import request
from rest_framework import exceptions, serializers
from django.db import transaction
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from users.models import UserInfo, Gender


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3, max_length=100, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(min_length=10, max_length=11, write_only=True)
    login_type = serializers.CharField(write_only=True, max_length=30)

    def validate(self, attrs):
        phone = attrs['phone']
        
        if not re.match('^\d{11}', phone) and not re.match('^\d{10}', phone):
            raise serializers.ValidationError({'phone': ('phone must be 10 or 11 digits')})

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username']
        )
        user_info = UserInfo.objects.create(
            user = user,
            login_type = validated_data['login_type']
        )
        return user
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'login_type')


class UserInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length = 5)
    age_group = serializers.ListField(required=False, child=serializers.CharField(), allow_empty=True)
    city = serializers.ListField(required=False, child=serializers.CharField(), allow_empty=True)
    gender = serializers.ChoiceField(required=False, choices = Gender.GENDER_CHOICES,allow_null=True)
    class Meta:
        model = UserInfo
        fields = ('id', 'name', 'age_group','city', 'gender')














