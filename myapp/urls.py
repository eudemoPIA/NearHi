from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import send_verification_code

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('category/<str:category>/', views.homepage, name='filtered_events'),
    path('search/', views.homepage, name='search_results'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('send-code/', send_verification_code, name='send_verification_code'),

    path('events/create/', views.create_event, name='create_event'),  
    path('events/<int:pk>/', views.event_detail, name='event_detail'),  
    path('events/save/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),  
    path('events/<int:pk>/apply/', views.apply_event, name='apply_event'),

    path('favorites/saved/', views.saved_events, name='saved_events'),
    path('favorites/upcoming/', views.upcoming_events, name='upcoming_events'),
    path('my-events/', views.my_events, name='my_events'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
