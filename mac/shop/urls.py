from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.shopping,name='shopping'),
    path('about/',views.about,name='AboutUs'),
    path('contact/',views.contact,name='ContactUs'),
    path('tracker/',views.tracker,name='TrackingStatus'),
    path('products/<int:myid>', views.product, name='ProductView'),
    path('checkout/', views.checkout, name='Checkout'),
    path('search/', views.search, name='Search'),
    path('handlerequest/', views.handlerequest, name='handlerequest'),
]
