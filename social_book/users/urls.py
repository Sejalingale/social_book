from django.contrib import admin
from django.urls import path
from users import views

urlpatterns = [
    path('',views.loginPage, name="login"),
    path('register/',views.register, name="register"),
    path('login/', views.loginPage, name='login'),
    path('index/',views.index,name='index'),
    path('reg/',views.reg, name="reg"),
    path('logout/',views.logoutPage,name='logout')
]