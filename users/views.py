from random import randint
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.core.cache import cache

from users.serializers import RegisterSerializer
from users.services import UserServices


class Register(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    authentication_classes = ()
    serializer_class = RegisterSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', None)
        cert_number = request.data.get('cert_number', None)
        print(UserServices().validate_cert_number(phone, cert_number))
        if UserServices().validate_cert_number(phone, cert_number):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data= {'error' : 'invalid-cert-number'}, status = status.HTTP_400_BAD_REQUEST)



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



