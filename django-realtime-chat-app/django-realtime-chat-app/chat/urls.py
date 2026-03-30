from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('room/<str:username>/', views.room, name='room'),
]
