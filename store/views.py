from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookie_cart, cart_data, guest_order
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import UserRegisterForm

def store(request):
    data = cart_data(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems, 'shipping':False}
    return render(request, 'store/cart.html', context)

def checkout(request):
    data = cart_data(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)

    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <=0: 
        orderItem.delete()

    return JsonResponse('Item was added', safe = False)

@ csrf_exempt
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated: 
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)

    else: 
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    # checks total value of data submitted is equal to cart total
    # this makes sure that someone that manipulates the data in the console can't 
    # process the transaction
    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer, 
            order = order, 
            address = data['shipping']['address'], 
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )
    
    return JsonResponse('Payment complete!', safe = False)

def about(request):
    return render(request, 'store/about.html', {'title':'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # contains username and 2 passwords that user enter
        
        if form.is_valid(): # checks if data is valid, if valid, this conditional statement will create an account
            form.save() # saves user info database
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1') 
            user = authenticate(username = username, password = password)
            Customer.objects.create(user = user, name = user.username, email = user.email)
            login(request, user)
            messages.success(request, f'Your account has been created! You are now able to log in') # displays message if form data is valid
            return redirect('store') 
    else: 
        form = UserRegisterForm()

    return render(request, 'store/register.html', {'form' : form})