from email import message
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from matplotlib.style import context
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.views.decorators.csrf import csrf_protect
from .restapis import *
import requests
from django.contrib.auth.decorators import login_required

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://0ebccdee.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        # dealer_names = " ".join([dealer.short_name for dealer in dealerships])
        # return HttpResponse(dealerships)
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
            messages.error(
                request, 'User does not exist. Please sign up for an account.')
            return redirect('djangoapp:index')

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('djangoapp:index')
        ...
    else:
        messages.error(
            request, 'Username or Password is incorrect. Please try again.')
        return redirect('djangoapp:index')
        ...

# Create a `logout_request` view to handle sign out request


def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request


def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
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
                messages.warning(
                    request, 'Please insert a valid username and password.')
                return render(request, 'djangoapp/registration.html')
            else:
                user = User.objects.create_user(
                    username=username, password=password, first_name=first_name, last_name=last_name)
                user.save()
                login(request, user)
                messages.success(
                    request, f'Welcome {username}. You are successfully logged in.')
                return render(request, 'djangoapp/index.html')
        else:
            messages.error(request, 'User already exists.')
            return render(request, 'djangoapp/index.html')


# Update the `get_dealerships` view to render the index page with a list of dealerships


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {}

    if request.method == "GET":
        url = "https://0ebccdee.eu-gb.apigw.appdomain.cloud/api/review"
        url_2 = "https://0ebccdee.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealership_name = get_request(url_2, id=dealer_id)[
            'body']['docs'][0]['full_name']
        dealership_id = get_request(url_2, id=dealer_id)[
            'body']['docs'][0]['id']
        review_results = get_dealer_reviews_from_cf(
            url, dealer_id=dealer_id)
        context['dealer_details'] = review_results
        context['dealership_name'] = dealership_name
        context['dealership_id'] = dealership_id
        print(review_results)
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review


@login_required
@csrf_protect
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        url_2 = "https://0ebccdee.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealership_details = get_request(url_2, id=dealer_id)[
            'body']['docs'][0]
        context['dealership_name'] = dealership_details['full_name']
        context['dealer_id'] = dealership_details['id']
        carmodels = CarModel.objects.filter(dealership_id=dealer_id)
        context['carmodels'] = carmodels

        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == "POST":
        url = "https://0ebccdee.eu-gb.apigw.appdomain.cloud/api/review"
        user = request.user
        review = {}
        car_id = request.POST['car-model-selection']
        car = CarModel.objects.get(id=car_id)
        review['name'] = user.username
        review['dealership'] = dealer_id
        review['review'] = request.POST['reviewcontent']
        review['purchase'] = False
        review['purchase_date'] = request.POST['purchasedate']
        review['car_make'] = car.make.name
        review['car_model'] = car.name
        review['car_year'] = car.year
        json_payload = {}
        json_payload["review"] = review
        print(json_payload['review'])
        response = post_request(url, json=json_payload['review'])
        return redirect('djangoapp:dealer_details', dealer_id)
