from django.contrib import admin
from django.urls import path , include

from . import views


urlpatterns = [
        path('meeting/',views.videoCall, name = 'videoCall'),
        path('join/',views.join_room, name = 'join_room'),
]