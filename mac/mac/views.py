from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import  messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
import math, random

def home(request):
        return render(request,"accounts/home.html")
