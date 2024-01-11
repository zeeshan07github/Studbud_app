from django.urls import path 
from . import views

# app_name = 'studbud'
urlpatterns = [
    path('' , views.home  , name = 'home'),
    path('room/<str:pk>/' , views.ROOM , name = 'room'),
    path('profile/<str:pk>/' , views.profile , name = 'profile'),
    path('update_user/' , views.updateUser , name = 'update_user'),
    path('create_room/' , views.create_room , name = 'create_room'),
    path('edit_room/<str:pk>/' , views.editroom , name = 'edit_room'),
    path('delete_room/<str:pk>/' , views.delete_room , name = 'delete_room'),
    path('delete_message/<str:pk>/' , views.delete_message , name = 'delete_message'),
    path('login/' , views.logedin , name = 'login') ,
    path('logout/' , views.logedout , name = 'logout') ,
    path('register/' , views.register , name = 'register') ,
    path('topics/' , views.topics , name = 'topics') ,
    path('activity/' , views.activity , name = 'activity') ,



]
