from django.urls import path
from . import views

urlpatterns = [
    path('filtered/<str:category>/', views.filtered_events, name='filtered_events'),
    path('post/', views.post_event, name='post_event'),
]
