

from users import views
from django.urls import path


urlpatterns=[
    path(r'register', views.Register.as_view(), name='register'),
    path(r'cert-number', views.Cert_number.as_view(), name ='cert-number'),
    path(r'cert-number/validate', views.Validate_cert_number.as_view(), name = 'validate-cert-number')
]