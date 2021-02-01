from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signupuser/', views.signupuser, name='signupuser'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('logoutuser', views.logoutuser, name='logoutuser'),
]