"""
URL configuration for danlis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', base, name='base'),
    path('index/', index, name='index'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', Login, name='login'),
    path('register/', register, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
    path('analisis/', analisis, name='analisis'),
    path('logout/', logout, name='logout'),
    path('profile/', profile, name='profile'),
    path('analisis/detil/<int:upload_id>/detail/', detail_upload, name='detail_upload'),
    path('analisis/detil/<int:upload_id>/hapus/', hapus_upload, name='hapus_upload'),

]
