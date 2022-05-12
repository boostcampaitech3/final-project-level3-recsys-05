from xml.etree.ElementInclude import include
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index),
    path('create/', views.create),
    path('read/id/', views.read),
    path('result/', views.result, name = 'result')
]
