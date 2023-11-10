from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.chat_room, name='chat_room'),
    path('chat/<str:room_name>/', views.room, name='room'),
]