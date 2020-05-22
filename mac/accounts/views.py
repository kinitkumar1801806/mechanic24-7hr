from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import  messages
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.conf import settings
import math, random,string
from .models import User_Accounts,Mechanic_Accounts,Contact
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from math import ceil
from twilio.rest import Client
import os

def home1(request):
    return render(request,'accounts/home.html')

def msignup(request):
    global otp
    if request.method=="POST":
        uname=request.POST.get('username','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        aadhar=request.POST.get('aadhar','')
        address=request.POST.get('address','')
        pass1=request.POST.get('password1','')
        pass2=request.POST.get('password2','')
        fname=request.POST.get('firstname1','')
        lname=request.POST.get('lastname1','')
        if len(uname)<4 or len(uname)>15 or not uname.isalnum():
            messages.error(request,"Username Should be greater than 4 and less than 15 and should contain letters and numbers")
            return redirect('home1')
        if len(phone)<10 or len(phone)>10:
            messages.error(request,"Please enter a valid phone number")
            return redirect('home1')
        if len(pass1)<8 :
            messages.error(request,"Password should be greater than 8 and less than 15 amd should contain letters and numbers ")
            return redirect('home1')
        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return redirect('home1')
        if len(aadhar)<16:
            messages.error(request,"Please enter a valid aadhar number")
            return redirect('home1')
        otp=generateOTP()
        print(otp)
        params={'uname':uname,'email':email,'phone':phone,'pass1':pass1,'address':address,'aadhar':aadhar,'fname':fname,'lname':lname}
        print(params)
        send_mail(
        'Subject here',
        'Plese verify your email address by using this one time password'+otp,
        settings.EMAIL_HOST_USER,
        [email],
    fail_silently=False,
)
    return render(request, 'accounts/emailverify.html',params)

def mlogin(request):
    if request.method=="POST":
        uname=request.POST.get('username','')
        pass1=request.POST.get('password','')
        mid=request.POST.get('mid','')
        mechanic=Mechanic_Accounts.objects.all()
        float=0
        for md in mechanic:
          if md.mechanic_id == mid:
             float=1
        if float==0:
            messages.error(request,"There is no mechanic with this mechanic id.Please enter correct mechanic id.")
            return redirect("home1")
            
        if float==1:     
             user=authenticate(username=uname,password=pass1)
             if user is not None:
                 login(request,user)
                 luser=Mechanic_Accounts.objects.all()
                 for lu in luser:
                     if lu.mymechanic.username == user.username:
                         image=lu.image
                         params={'add':add,'phone':phone,'image':image}
                     else:
                         messages.error(request,"Please enter correct login Credentials.If not registered,register first.")
                         return redirect('home1')
    return render(request,'accounts/welcome_mechanic.html',params)


def usignup(request):
    global otp
    if request.method=="POST":
        uname=request.POST.get('username','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        pass1=request.POST.get('password1','')
        address=request.POST.get('address','')
        pass2=request.POST.get('password2','')
        fname=request.POST.get('firstname','')
        lname=request.POST.get('lastname','')
        if len(uname)<4 or len(uname)>15 or not uname.isalnum():
            messages.error(request,"Username Should be greater than 4 and less than 15 and should contain letters and numbers")
            return redirect('home1')
        if len(phone)<10 or len(phone)>10:
            messages.error(request,"Please enter a valid phone number")
            return redirect('home1')
        if len(pass1)<8:
            messages.error(request,"Password should be greater than 8 and less than 15 amd should contain letters and numbers ")
            return redirect('home1')
        if pass1 != pass2:
            messages.error(request,"Password do not match")
            return redirect('home1')
        otp=generateOTP()
        print(otp)
        params={'uname':uname,'email':email,'phone':phone,'pass1':pass1,'address':address,'fname':fname,'lname':lname}
        send_mail(
        'This is an email from Puncher.Com',
        'Plese verify your email address by using this one time password'+otp,
        settings.EMAIL_HOST_USER,
        [email],
    fail_silently=False,
)
    return render(request, 'accounts/Email.html',params)

def ulogin(request):
    if request.method=="POST":
        uname=request.POST.get('username','')
        pass1=request.POST.get('password','')
        user=authenticate(username=uname,password=pass1)
        if user is not None:
            login(request,user)
            luser=User_Accounts.objects.all()
            for lu in luser:
               if lu.myuser.username == user.username:
                    add=lu.address
                    phone=lu.phone
                    image=lu.image
                    params={'add':add,'phone':phone,'image':image}
        else:
            messages.error(request,"Please enter correct login Credentials.If not registered,register first.")
            return redirect('home1')
    return render(request, 'accounts/welcome_user.html',params)

def generateOTP() :

    # Declare a digits variable
    # which stores all digits
    digits = "0123456789"
    OTP = ""

   # length of password can be chaged
   # by changing value in range
    for i in range(6) :
        OTP += digits[math.floor(random.random() * 10)]

    return OTP

def everify(request):
    if request.method=="POST":
        code=request.POST.get('code','')
        uname=request.POST.get('username','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')
        fname=request.POST.get('firstname','')
        lname=request.POST.get('lastname','')
        if code!=otp:
            messages.error(request,"Please enter the correct code")
            return redirect('everify')
        user=User.objects.create_user(username=uname,email=email,password=password,first_name=fname,last_name=lname)
        user.save()
        user_signup=User_Accounts(myuser=user,address=address,phone=phone,image="/media/shop/images/cylinder1.jpg")
        user_signup.save()
        messages.success(request,"You are successully signed up")
    return render(request,"accounts/home.html")
def verify(request):
    global mid
    if request.method=="POST":
        code=request.POST.get('code','')
        uname=request.POST.get('username','')
        email=request.POST.get('email','')
        password=request.POST.get('password','')
        phone=request.POST.get('phone','')
        address=request.POST.get('address','')
        aadhar=request.POST.get('aadhar','')
        fname=request.POST.get('firstname','')
        lname=request.POST.get('lastname','')
        mid=id_generator()
        print(mid)
        if code!=otp:
            messages.error(request,"Please enter the correct code")
            return redirect('meverify')
        send_mail(
        'This is an email from Puncher.Com',
        'Your mechanic id is '+mid,
        settings.EMAIL_HOST_USER,
        [email],
    fail_silently=False,
)
        mechanic=User.objects.create_user(username=uname,email=email,password=password,first_name=fname,last_name=lname)
        mechanic.save()
        mechanic_signup=Mechanic_Accounts(mymechanic=mechanic,address=address,aadhar=aadhar,mechanic_id=mid,phone=phone,image="/media/shop/images/cylinder1.jpg")
        mechanic_signup.save()
        messages.success(request,"You are successully signed up as a mechanic")
    return render(request,"accounts/home.html")

def id_generator(size=8, chars=string.digits+string.ascii_uppercase + string.digits):
       return ''.join(random.choice(chars) for _ in range(size))

def logout1(request):
    logout(request)
    messages.success(request,"You are successfully logged out")
    return redirect('home')

def wuser(request):
    luser=User_Accounts.objects.all()
    for lu in luser:
        if lu.myuser.username == request.user.username:
            add=lu.address
            phone=lu.phone
            image=lu.image
            dob=lu.dob
            bio=lu.bio
            vehicle=lu.vehicle
            model=lu.model
            params={'add':add,'phone':phone,'image':image}
    return render(request,'accounts/welcome_user.html',params)

def wmechanic(request):
    luser=Mechanic_Accounts.objects.all()
    for lu in luser:
        if lu.mymechanic.username == request.user.username:
            add=lu.address
            phone=lu.phone
            image=lu.image
            aadhar=lu.aadhar
            ratings=lu.ratings
            mid=lu.mechanic_id
            expertat=lu.expertat
            totalcustomer=lu.totalcustomer
            totalsatisfiedcustomer=lu.totalsatisfiedcustomer
            timeperiod=lu.timeperiod
            Experience=lu.Experience
            amt=lu.avg_amt
            bio=lu.bio
            dob=lu.dob
            params={'add':add,'phone':phone,'image':image,'aadhar':aadhar,'ratings':ratings,'mid':mid,
            'expertat':expertat,'totalcustomer':totalcustomer,'totalsatisfiedcustomer':totalsatisfiedcustomer,
            'timeperiod':timeperiod,'Experience':Experience,'amt':amt,'bio':bio,'dob':dob}       
    return render(request,'accounts/welcome_mechanic.html',params)

def uprofile(request):
    luser=User_Accounts.objects.all()
    for lu in luser:
        if lu.myuser.username == request.user.username:
                add=lu.address
                phone=lu.phone
                image=lu.image
                dob=lu.dob
                bio=lu.bio
                vehicle=lu.vehicle
                model=lu.model
                params={'add':add,'phone':phone,'image':image,'dob':dob,'bio':bio,'vehicle':vehicle,'model':model}
    return render(request,'accounts/user_profile.html',params)

def mechanics(request):
    allProds = []
    catprods = Mechanic_Accounts.objects.values('expertat','id')
    cats = {item['expertat'] for item in catprods}
    for cat in cats:
        prod = Mechanic_Accounts.objects.filter(expertat=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    print(params)
    return render(request, 'accounts/mechanics.html',params)


def mechanicview(request,myid):
    mechanic=Mechanic_Accounts.objects.filter(id=myid)
    return render(request,'accounts/mechanicview.html',{'mechanic':mechanic[0]})

def searchMatch(query,item):
    if query  in item.bio.lower() or query  in item.mymechanic.username.lower() or query  in item.mymechanic.first_name.lower():
        return True
    else:
       return False

def search(request):
    query=request.GET.get('search')
    allmechs = []
    catmechs = Mechanic_Accounts.objects.values('expertat', 'id')
    cats = {item['expertat'] for item in catmechs}
    for cat in cats:
        mechItem = Mechanic_Accounts.objects.filter(expertat=cat)
        mech=[item for item in mechItem if searchMatch(query,item)]
        n = len(mech)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(mech) != 0:
           allmechs.append([mech, range(1, nSlides), nSlides])
    params = {'allmechs': allmechs,'msg':''}
    if len(allmechs) == 0 or len(query)<4:
        params = { 'msg': 'Please make sure to enter relevant search query'}
    return render(request, 'accounts/search.html', params)

def track(request):
    return render(request,"accounts/track.html")

def addcontact(request,myid):
    user_name=request.user.username
    mechanic=Mechanic_Accounts.objects.filter(id=myid)
    mechanic_name=mechanic[0].mymechanic.username
    mechanic_id=mechanic[0].mechanic_id
    contacts=Contact.objects.filter(user_name=request.user.username)
    for con in contacts:
         mid=con.mechanic_id
         mechanic=Mechanic_Accounts.objects.filter(mechanic_id=mid)
         if mechanic[0].mymechanic.username==mechanic_name:
            messages.error(request,"Already added to your contact list")
            return redirect('mechanics')
    contact=Contact(user_name=user_name,mechanic_name=mechanic_name,mechanic_id=mechanic_id)
    contact.save()
    messages.success(request,"Successfully added the mechanic in your contact list")
    return redirect('mechanics')

def contacts(request):
     allmech=[]
     contacts=Contact.objects.filter(user_name=request.user.username)
     for con in contacts:
         mid=con.mechanic_id
         mechanic=Mechanic_Accounts.objects.filter(mechanic_id=mid)
         for mech in mechanic:
               allmech.append(mech)   
     page = request.GET.get('page', 1)
     paginator = Paginator(allmech, 1)
     try:
        photos = paginator.page(page)
     except PageNotAnInteger:
        photos = paginator.page(1)
     except EmptyPage:
        photos = paginator.page(paginator.num_pages)            
     return render(request,"accounts/contacts.html",{'allmech':allmech,'photos':photos})    

def remove(request,myid):
   if request.method=='POST':
       name=request.POST.get('mechanic'+ str(myid))     
       contacts=Contact.objects.filter(mechanic_name=name).delete()
   return redirect('contacts')  

def comment(request,myid):
    if request.method=='POST':
        name=request.POST.get('mechanic'+str(myid))
        rate=request.POST.get('rating'+str(myid))
        satisfy=request.POST.get('satisfaction'+str(myid))
        mech_id=request.POST.get('mech_id'+str(myid))
        mechanic=Mechanic_Accounts.objects.all()
        for mech in mechanic:
           if mech.mechanic_id==mech_id:
              if mech.mymechanic.username==name:
                mech.totalcustomer=mech.totalcustomer+1
                mech.ratings=((mech.ratings*(mech.totalcustomer-1))+float(rate))/mech.totalcustomer
                if satisfy=="Yes":
                    mech.totalsatisfiedcustomer=mech.totalsatisfiedcustomer+1
                mech.save()  
                messages.success(request,"Successfully commented")
                return redirect('contacts')  
           
        messages.error(request,"Please enter the correct mechanic id in order to comment the profile")
        return redirect('contacts')           
    return redirect('contacts')   

def changepassword(request):
    return render(request,"accounts/ChangePassword.html")   
def change_password(request):
    if request.method=="POST":
        old_pass=request.POST.get('oldpass','')
        new_pass1=request.POST.get('newpass','')
        new_pass2=request.POST.get('confirmpass','')
        user1=authenticate(username=request.user.username,password=old_pass)
        if user1 is  None:
              messages.error(request,"Please Enter the Correct old password")
              return redirect('changepassword')
        if len(new_pass1)<8 :
            messages.error(request,"Password should be greater than 8 and less than 15")
            return redirect('changepassword')
        if new_pass1 != new_pass2:
            messages.error(request,"Password do not match")
            return redirect('changepassword')
        users=User.objects.get(username=request.user.username)
        users.set_password(new_pass1)
        print(users)
        users.save()
        user=authenticate(username=request.user.username,password=new_pass1)
        if user is not None:
            login(request,user)
            messages.success(request,"You have successully changed your password")
            return redirect('wuser')
    return redirect('wuser')            

def update_profile(request):
    global otp1
    if request.method=="POST":
      first_name=request.POST.get('firstname','')
      last_name=request.POST.get('lastname','')
      email=request.POST.get('email','')
      phone=request.POST.get('phone','')
      dob=request.POST.get('dob','')
      address=request.POST.get('address','')
      bio=request.POST.get('bio','')
      vehicle=request.POST.get('vehicle','')
      model=request.POST.get('model','')
    users=User_Accounts.objects.all()
    for us in users:
        if us.myuser.username==request.user.username:
            us.bio=bio
            us.address=address
            us.dob=dob
            us.vehicle=vehicle
            us.model=model
            us.save()
    users=User.objects.get(username=request.user.username)
    users.email=email
    users.firstname=first_name
    users.lastname=last_name
    users.save()
    otp1=generateOTP()
    account_sid = 'ACc1f37b81f1c1964d0c948a0d4bf1c391'
    auth_token = 'c762aea7a7f7815baa8f4a4f5d5a02e9'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
         body='This is an sms from Punchter.Com.'+otp1+' is the one time password to verify your phone number',
         from_='+12058595072',
         to='+919006317054'
     )
    print(message.sid)
    return render(request,'accounts/verify_phone.html',{'phone':phone})
def verify_phone(request):
    if request.method=="POST":
        code=request.POST.get('code','')
        phone=request.POST.get('phone','')
        if code==otp1:
            users=User_Accounts.objects.all()
            for us in users:
                if us.myuser.username==request.user.username:
                    us.phone=phone
                    us.save()
                    messages.success(request,"Your profile is updated")
                    return redirect('uprofile') 
        else:
          messages.error(request,"Please enter the valid otp") 
          return redirect('verify_phone')           
    return redirect('uprofile')    

def upload_image(request):
   if request.method=="POST":
     img=request.FILES['image']

   users=User_Accounts.objects.all() 
   for us in users:
      if us.myuser.username==request.user.username: 
         us.image=img
         us.save()
   return redirect('uprofile')    