from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import analyze_review_sentiments, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, get_dealers_by_state_from_cf, get_dealers_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os
from dotenv import load_dotenv
import uuid

load_dotenv()

# Cloud Functions API configuration values
cf_api_base_url = os.environ['cf_api_base_url']


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


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
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = cf_api_base_url + "/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        # Temporary code to add cars to each dealership
        # make = CarMake.objects.get(id=2)
        # for dealer in dealerships:
        #     car = CarModel(car_make = make, name = "X5", dealer_id = dealer.id, type = "sport", year = datetime.utcnow().date())
        #     car.save()
        # return HttpResponse("success")

        # Return a list of dealers
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = cf_api_base_url + "/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state_from_cf(url, state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        # Get dealer from the URL
        url = cf_api_base_url + "/dealership"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)
        # Get reviews from API
        url = cf_api_base_url + "/review"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Add objects to context and render template
        context["dealer"] = dealer
        context['review_list'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "GET":
        # Check if user is logged in
        if(request.user.is_authenticated): 
            # Get dealer from API
            url = cf_api_base_url + "/dealership"
            dealer = get_dealer_by_id_from_cf(url, dealer_id)
            
            # Get cars associated with dealer
            dealer_car_list = CarModel.objects.filter(dealer_id=dealer_id).all()
            
            # Add objects to context and render template
            context["dealer"] = dealer
            context['cars'] = dealer_car_list
            return render(request, 'djangoapp/add_review.html', context)
        
        else:
            context['message'] = "You need to login first."
            return render(request, 'djangoapp/login.html', context)

    if request.method == "POST":
        # Check if user is logged in
        if(request.user.is_authenticated):          
            # Create a review object
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["dealership"] = dealer_id
            review["id"] = uuid.uuid4().hex
            review["name"] = request.user.first_name + " " + request.user.last_name
            review["review"] = request.POST['content']
            
            # Retrieve purchase information based on checkbox
            purchase = False
            if 'purchasecheck' in request.POST:    
                purchase = True
                
            review["purchase"] = purchase
            
            if purchase:
                review["purchase_date"] = request.POST['purchasedate']
            
                # Retrieve car information based on id
                car_id = request.POST['car']
                car = CarModel.objects.get(id=car_id)
                review["car_make"] = car.car_make.name
                review["car_model"] = car.name
                review["car_year"] = car.year.strftime("%Y")

            # Create the json payload for the request
            json_payload = dict()
            json_payload["review"] = review
            
            # Call the service to post the review
            url = cf_api_base_url + "/review"
            response = post_request(url=url, json_payload=json_payload, dealerId=dealer_id)

            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

        else:
            context['message'] = "You need to login first."
            return render(request, 'djangoapp/login.html', context)

