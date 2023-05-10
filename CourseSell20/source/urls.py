from django.contrib import admin
from django.urls import path, include

from source import views

urlpatterns = [
    path("", views.main, name="main"),
    path("profile/", views.profile, name="profile"),

               ]
