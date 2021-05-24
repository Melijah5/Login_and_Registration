from django.urls import path

from . import views

urlpatterns = [
    
    path('', views.index),
    path("login", views.register),
    path("homepage", views.homepage),
    path("logout", views.logout),
    path("user-login", views.user_login),
]