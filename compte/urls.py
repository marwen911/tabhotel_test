from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('loginn',loginn,name='loginn'),
    path('register',register,name='register'),
    path('success',success,name='success'),
    path('token',token_send,name='token_send'),
    path('verify/<auth_token>',verify,name='verify'),
    path('error',error_page,name='error'),
    path('accounts/', include('django.contrib.auth.urls')),
    path ('link/<int:id>',link,name='link'),




]
