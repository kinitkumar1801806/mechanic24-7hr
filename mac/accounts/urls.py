from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home1,name='home1'),
    path('mechanic_signup/',views.msignup,name='msignup'),
    path('mechanic_login/',views.mlogin,name='mlogin'),
    path('user_signup/',views.usignup,name='usignup'),
    path('user_login/',views.ulogin,name='ulogin'),
    path('verify_email/',views.everify,name='everify'),
    path('email_verify/',views.verify,name='verify'),
    path('logout1/',views.logout1,name='logout1'),
    path('welcome_user/',views.wuser,name="wuser"),
    path('welcome_mechanic/',views.wmechanic,name="wmechanic"),
    path('user_profile/',views.uprofile,name='uprofile'),
    path('mechanics/',views.mechanics,name="mechanics"),
    path('mechanicview/<int:myid>',views.mechanicview,name="mechanicview"),
    path('search/',views.search,name="search"),
    path('addcontact/<int:myid>',views.addcontact,name="addcontact"),
    path('track/',views.track,name="track"),
    path('contacts/',views.contacts,name="contacts"),
]
