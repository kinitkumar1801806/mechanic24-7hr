from django.shortcuts import render, redirect
from .models import Products, Contact, Orders, OrderUpdate,Payment_history
from math import ceil
import json
from django.contrib import  messages
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'z6Jg2Eq466bmF0Wr'

def shopping(request):
    allProds = []
    catprods = Products.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Products.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success','updates':updates,'itemsJson':order[0].orders_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')

def searchMatch(query,item):
    if query  in item.desc.lower() or query  in item.category.lower() or query  in item.product_name.lower():
        return True
    else:
       return False

def search(request):
    query=request.GET.get('search')
    allProds = []
    catprods = Products.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodItem = Products.objects.filter(category=cat)
        prod=[item for item in prodItem if searchMatch(query,item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
           allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds,'msg':''}
    if len(allProds) == 0 or len(query)<4:
        params = { 'msg': 'Please make sure to enter relevant search query'}
    return render(request, 'shop/search.html', params)


def product(request, myid):

    # Fetch the product using the id
    product = Products.objects.filter(id=myid)
    return render(request, 'shop/prod.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        if len(zip_code)<6:
             messages.error(request,"Please enter correct zip code")
             return redirect('Checkout')
        if len(phone)<10:
             messages.error(request,"Please enter correct phone number")
             return redirect('Checkout')     

        order = Orders(orders_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

                'MID': 'Ljlxjc16845781456724',
                'ORDER_ID': str(order.order_id),
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01': 
            if request.user.id!=None:
                histroy=Payment_history(mail=request.user.email,payment_json=response_dict)
                histroy.save()
            print('Order successful')
        else:
            messages.error(request,'Order was not successful because' + response_dict['RESPMSG'])
            return redirect('Checkout')
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def user_history(request):
    history = Payment_history.objects.filter(mail=request.user.email)
    for hr in history:
         return render(request, 'shop/user_payment_history.html',{'allpayments':hr.payment_json})
