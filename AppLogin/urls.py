from django.urls import re_path
from AppLogin.views import *

urlpatterns = [
    re_path('Login', LoginView, name='Login'),
    re_path('Logout', LogoutView, name='Logout'),
    re_path('register_user', RegisterUser, name='RegisterUser'),

]
