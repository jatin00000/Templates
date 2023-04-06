"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from mimetypes import init
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from unicodedata import name
from django.contrib import admin
from django.urls import path
from . import views
from .views import MyTokenObtainPairView
from user import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('init/date', views.start_date.as_view(), name='init_date'),
    path('init/status_code', views.start_status.as_view(), name='init_status_code'),
    path('init/type', views.start_type.as_view(), name='init_type'),
    path('search', views.search.as_view(), name='search'),
    path('init', views.start.as_view(), name="init"),
    path('',view.SignupPage, name="signup"),
    path('loginU',view.LoginPage, name="login"),
    path('home',view.HomePage, name="home"),
    path('logout', view.LogoutPage, name="logout"),
    path('token', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
]
