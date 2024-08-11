from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name = 'login'),
    path('register/', views.register_view, name='register'),
    path('sned_verification_code/', views.send_verification_code, name='sned_verification_code'),
]
