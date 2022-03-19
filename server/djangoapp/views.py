from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import analyze_review_sentiments, get_dealer_reviews_from_cf, get_dealers_by_state_from_cf, get_dealers_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import os
from dotenv import load_dotenv

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
        url = cf_api_base_url + "/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


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
        url = cf_api_base_url + "/review"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all reviews
        reviews_list = ' '.join([review.review for review in reviews])
        # Return a list of reviews
        return HttpResponse(reviews_list)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    if request.method == "POST":
        # Check if user is logged in
        if(request.user.is_authenticated):
            url = cf_api_base_url + "/review"
            # Create a review object
            review = dict()
            review["time"] = datetime.utcnow().isoformat()
            review["car_make"] = "Audi",
            review["car_model"] = "Car",
            review["car_year"] = 2022,
            review["dealership"] = 29,
            review["id"] = 1114,
            review["name"] = "John Doe",
            review["purchase"] = True,
            review["purchase_date"] = "02/01/2022",
            review["review"] = "This was the fastest I have ever been in and out of a dealership. The Rep was extremely helpful and got me a great car. He listened to what I wanted and didn't go over my monthly payments."
            # Create the json payload for the request
            json_payload = dict()
            json_payload["review"] = review
            # Call the service to post the review
            response = post_request(url=url, json_payload=json_payload, dealerId=dealer_id)

            return HttpResponse(response)

        else:
            context['message'] = "You need to login first."
            return render(request, 'djangoapp/login.html', context)


