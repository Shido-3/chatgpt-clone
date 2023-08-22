from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot, name='chatbot'), # main/home page, "views.chatbot" is the function that is called when the url is visited
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
]

# Technically this is the first file to get executed because the main page is located here