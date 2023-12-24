from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Pizza, Burger, Order, Item
from .forms import NewUserForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import HttpResponse
import random
import json

def randomOrderNumber(length):
    sample = 'ABCDEFGH0123456789'
    numberO = ''.join((random.choice(sample) for i in range(length)))
    return numberO


# Create your views here.

def index(request):
    request.session.set_expiry(0)
    context = {
        'active_link': 'index'
    }
    return render(request, 'food/index.html', context)

def pizza(request):
    request.session.set_expiry(0)
    pizzas = Pizza.objects.all()
    context = {
        'pizzas': pizzas,
        'active_link': 'pizza'
    }
    return render(request, 'food/pizza.html', context)
 
def burger(request):
    request.session.set_expiry(0)
    burgers = Burger.objects.all()
    context = {
        'burgers': burgers,
        'active_link': 'burger'
    }
    return render(request, 'food/burgers.html', context)

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@csrf_exempt
def order(request):
    request.session.set_expiry(0)
    if is_ajax(request):
        request.session['note'] = request.POST.get('note')
        request.session['order'] = request.POST.get('orders')
        orders = json.loads(request.session['order'])
        request.session['bill'] = request.POST.get('bill')
        randomNum = randomOrderNumber(6)

        while Order.objects.filter(number=randomNum).count() > 0:
            randomNum = randomOrderNumber(6)

        if request.user.is_authenticated:
            order = Order(
                customer=request.user, 
                number=randomOrderNumber(6), 
                bill=float(request.session['bill']), 
                note=request.session['note']
            )
            order.save()
            request.session['orderNum'] = order.number
            for article in orders:
                item = Item(
                    order = order,
                    name  = article[0],
                    price = float(article[2]),
                    size  = article[1]
                )
                item.save()
    context = {
        'active_link': 'order'
    }
    return render(request, 'food/order.html', context)

def success(request):
    orderNum = request.session['orderNum']
    bill = request.session['bill']
    items = Item.objects.filter(order__number=orderNum)
    context = {
        'orderNum': orderNum,
        'bill': bill,
        'items': items
    }
    return render(request, 'food/success.html', context)

def signup(request):
    context = {}
    if request.POST:
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            context['form'] = form
    else:
        form = NewUserForm()
        context['form'] = form
    return render(request, 'food/signup.html', context)

def logIn(request):
    if request.POST:
        username = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=username, password=pwd)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'username and/or password are incorrect')
    context = {
        'active_link': 'login'
    }
    return render(request, 'food/login.html', context)

def logOut(request):
    logout(request)
    return redirect('index')