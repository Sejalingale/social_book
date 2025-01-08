from django.contrib import admin
from django.urls import path,include
from users import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('',views.loginPage, name="login"),
    path('register/',views.register, name="register"),
    path('login/', views.loginPage, name='login'),
    path('index/',views.index,name='index'),
    path('logout/',views.logoutPage,name='logout'),
    path('authors-and-sellers/', views.authors_and_sellers, name='authors_and_sellers'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('upload/',views.upload_file,name='upload_file')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)