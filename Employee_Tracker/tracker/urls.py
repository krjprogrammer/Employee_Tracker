from django.urls import path
from .views import User_Registration,User_Login
urlpatterns = [
    path('register',User_Registration.as_view()),
    path('login',User_Login.as_view()),
]