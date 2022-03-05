from email import message
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist. Please sign up for an account.')
            return redirect('djangoapp:index')
        
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('djangoapp:index')
        ...
    else:
        messages.error(request, 'Username or Password is incorrect. Please try again.')
        return redirect('djangoapp:index')
        ...

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context={}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html',context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False

        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error('New User')
        
        if not user_exist:
            if username == "" or password == "":
                messages.warning(request, 'Please insert a valid username and password.')
                return render(request, 'djangoapp/registration.html')
            else:
                user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()
                login(request,user)
                messages.success(request,f'Welcome {username}. You are successfully logged in.')
                return render(request, 'djangoapp/index.html')
        else:
            messages.error(request,'User already exists.')
            return render(request, 'djangoapp/index.html')

        
        

# Update the `get_dealerships` view to render the index page with a list of dealerships



# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ..