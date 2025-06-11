from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('users/',views.user_list_view,name='user_list'),
    path('chat/<str:username>/',views.chat_room,name='chat_room'),
]
