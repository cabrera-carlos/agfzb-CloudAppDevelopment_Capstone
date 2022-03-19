import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Watson NLU API configuration values
watson_nlu_api_base_url = os.environ['watson_nlu_api_base_url']
watson_nlu_api_key = os.environ['watson_nlu_api_key']
watson_nlu_api_version = os.environ['watson_nlu_api_version']

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)   
    print("GET from {} ".format(url))
    api_key = ""
    
    if "api_key" in kwargs:
        api_key = kwargs["api_key"]
    
    try:
        if api_key:
            # Basic authentication GET
            # Only used for Watson NLU Service
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            
            response = requests.get(url, params=params, 
                                    headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', api_key))
        else:
            # Call get method of requests library with URL and parameters. No authentication
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    
    print(response.url)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
def post_request(url, json_payload, **kwargs):
    print(kwargs)   
    print("POST to {} ".format(url))

    # Call post method of requests library with URL and parameters.
    response = requests.post(url, params=kwargs, json=json_payload)

    print(response.url)
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


# Get dealers by state from a cloud function
def get_dealers_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the docs list in JSON as dealers
        dealers = json_result["docs"]
        # For each dealer object
        for dealer_doc in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            
            results.append(dealer_obj)

    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        # Get the docs list in JSON as dealers
        reviews = json_result["docs"]
        # For each review object
        for review_doc in reviews:
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"],purchase=review_doc["purchase"],
                                        review=review_doc["review"], purchase_date=review_doc["purchase_date"], 
                                        car_make=review_doc["car_make"], car_model=review_doc["car_model"],
                                        car_year=review_doc["car_year"], id=review_doc["id"])
            
            # Get the sentiment from Watson NLU Service
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            
            results.append(review_obj)

    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    url = watson_nlu_api_base_url + "/analyze"

    # Call get_request with a URL parameters for Watson NLU
    response = get_request(url
        , api_key = watson_nlu_api_key
        , text = text
        , version = watson_nlu_api_version
        , features = {"sentiment" : {}}
        , return_analyzed_text = True
    )

    # Get the sentiment label
    # If there is an error, return it formatted as a string
    if "error" in response:
        return "Error: {}".format(response["error"])
    else:
        text_sentiment = response["sentiment"]["document"]["label"]
        return text_sentiment
