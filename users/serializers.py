from rest_framework import exceptions, serializers
from django.db import transaction
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        min_length=3, max_length=30, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone = serializers.CharField(min_length=10, max_length=11, write_only=True)
    password = serializers.CharField(min_length=8, max_length=20, write_only=True)

    def validate(self, attrs):
        phone = attrs['phone']
        password = attrs['password']
        username = attrs['username']
        
        if not re.match('^\d{11}', phone) and not re.match('^\d{10}', phone):
            raise serializers.ValidationError({'phone': ('phone must be 10 or 11 digits')})
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({'password': (e.messages[0])})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'], password=validated_data['password'], email=validated_data['email']
        )
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'password', 'email')
