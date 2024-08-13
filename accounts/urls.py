from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('send_verification_code/', views.send_verification_code, name='send_verification_code'),
]
