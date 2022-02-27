from random import randint
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.core.cache import cache
from rest_framework.authtoken.models import Token

from users.serializers import RegisterSerializer, UserInfoSerializer
from users.services import UserServices
from rest_framework.authentication import TokenAuthentication
import json

class Register(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            print("EHRERERERE")
            data = UserServices().login(username)
            return Response(data = data, status = status.HTTP_200_OK)
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(data= {'error' : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)    




class Cert_number(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        cert_number = ''.join(["%s" % randint(0, 9) for num in range(0, 4)])
        UserServices().save_cert_number(phone, cert_number)
        message = "[kkanbu]\n 깐부 인증번호 : " + str(cert_number)
        try:
            UserServices().send_sms(phone, "인증번호", message)
        except Exception as e:
            return Response(data={'code' : "인증번호 발송실패"}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response(data={'cert-number' : cert_number}, status=status.HTTP_200_OK)


class Validate_cert_number(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        cert_number = request.data.get('cert_number', None)
        if cert_number == cache.get(phone, None):
            return Response(data= {'message' : "인증 성공"}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message' : 'wrong cert_number'}, status=status.HTTP_400_BAD_REQUEST)



class LoginPrevilege(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(data= {'message' : user.username}, status=status.HTTP_200_OK)




class RegionsList(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        f = open('regions.json')
        data = json.load(f)
        f.close()
        return Response(data = data['data'], status=status.HTTP_200_OK)

class SetProfile(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    serializer_class = UserInfoSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        user = request.user
        user_info = user.user_info
        serializer = self.get_serializer(user_info, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data= {'error' : serializer.errors}, status = status.HTTP_400_BAD_REQUEST)    
