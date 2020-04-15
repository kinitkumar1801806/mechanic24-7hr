from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('blogpost/<int:id>', views.blogpost, name='blogpost')
]
