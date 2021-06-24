import json
from django.urls.conf import path
from django.views.decorators.http import condition
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from .models import *
from .forms import RegisForm


# Create your views here.


def store(request):
    product = Product.objects.all()
    context = {'products': product}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(
            user=customer, statues=False)
        items = order.orderitems_set.all()
    else:
        items = {}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(
            user=user, statues=False)
        items = order.orderitems_set.all()
    else:
        items = {}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def register(request):
    form = RegisForm()
    if request.method == 'POST':
        data = request.POST
        form = RegisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Created')
            return redirect('login')
    context = {'form': form}
    return render(request, 'store/registration.html', context)


def loginpage(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("success")
            login(request, user)
            return redirect('home')
    return render(request, 'store/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')


def update_cart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    user = request.user
    product = Product.objects.get(id=productId)
    order, create = Order.objects.get_or_create(
        user=user, statues=False)
    orderitem, create = OrderItems.objects.get_or_create(
        order=order, product=product)
    if action == "add":
        orderitem.quantity = (orderitem.quantity + 1)
    if action == "remove":
        orderitem.quantity = (orderitem.quantity - 1)
    orderitem.save()
    if orderitem.quantity  <= 0 or action == 'remove_it':
        orderitem.delete()

    return JsonResponse('item added', safe=False)


def placeOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        user = request.user
        order, create = Order.objects.get_or_create(
            user=user, statues=False)
        print(order.statues)
        total = data['shippingInfo']['total']
        order.transaction_id = transaction_id
        if int(total) == order.get_cart_total:
            order.statues = True
            order.save()
            ShippingAddress.objects.create(
                user=user,
                order=order,
                address=data['shippingInfo']['address'],
                state=data['shippingInfo']['state'],
                city=data['shippingInfo']['city'],
                zipcode=data['shippingInfo']['zipcode'],
            )

    return JsonResponse('ORDERe PLACED', safe=False)


def myOrder(request):
    user = request.user
    try:
       orders = Order.objects.filter(user = user,statues = True)
    except:
        orders = {} 
    context = {'orders':orders}
    print(orders)
    return render(request,'store/orders.html',context) 

def update_myorder(request):
    data = json.loads(request.body)
    productId = data['productId']
    trans_id = data['trans_id']
    user = request.user
    product = Product.objects.get(id=productId)
    order = Order.objects.get(user = user ,transaction_id = trans_id)
    orderitem = OrderItems.objects.get(order = order,product = product)
    orderitem.delete()
    return JsonResponse('orderItem deleted ' ,safe=False)


def view(request,id):
    user = request.user
    product = Product.objects.get(id = id)
    context = {"product":product}
    return render(request,'store/view.html',context)