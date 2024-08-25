from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import custom_logout_view, send_verification_code

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('category/<str:category>/', views.filtered_events, name='filtered_events'),
    path('search/', views.search_results, name='search_results'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('send-code/', send_verification_code, name='send_verification_code'),
    path('logout/', custom_logout_view, name='logout'),

    path('events/create/', views.create_event, name='create_event'),  
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.edit_event, name='edit_event'),  
    path('events/save/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),  
    path('events/<int:pk>/apply/', views.apply_event, name='apply_event'),

    path('saved/', views.saved_events, name='saved_events'),
    path('upcoming/', views.upcoming_events, name='upcoming_events'),
    path('my-events/', views.my_events, name='my_events'),

    path('events/delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
    path('events/cancel-collection/<int:event_id>/', views.cancel_collection, name='cancel_collection'),
    path('events/cancel-application/<int:event_id>/', views.cancel_application, name='cancel_application'),
    ]
