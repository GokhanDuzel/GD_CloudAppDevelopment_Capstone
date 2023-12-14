import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions



# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, api_key=None, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if api_key:
        print('Houston we have an api key')
        response = requests.get(
            url, 
            params=kwargs, 
            headers={'Content-Type': 'application/json'},
            auth=HTTPBasicAuth('apikey', api_key)
        )
    else:
        print('Houston we DON"T have an api key')
        # Call get method of requests library with URL and parameters
        response = requests.get(
            url, 
            headers={'Content-Type': 'application/json'},
            params=kwargs
        )

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    response = requests.post(
        url,
        params=kwargs,
        data=json.dumps(json_payload),
        headers={'Content-Type': 'application/json'},
    )

    status_code = response.status_code
    print("With status {} ".format(status_code))
    print("Response text: ", response.text)

    try:
        json_data = json.loads(response.text)
        return json_data
    except json.JSONDecodeError:
        print("Error decoding JSON response")
        return None



# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, api_key=None)
    
    if isinstance(json_result, list):
        dealers = json_result
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_obj = CarDealer(
                address=dealer.get("address", ""),
                city=dealer.get("city", ""),
                full_name=dealer.get("full_name", ""),
                id=dealer.get("id", ""),
                lat=dealer.get("lat", ""),
                long=dealer.get("long", ""),
                short_name=dealer.get("short_name", ""),
                st=dealer.get("st", ""),
                zip=dealer.get("zip", "")
            )
            results.append(dealer_obj)

    return results

# def get_dealer_by_id_from_cf(url, dealerId):
def get_dealer_by_id_from_cf(url, dealer_id):
    json_result = get_request(url, id=dealer_id)
    if json_result:
        print(json_result,'dealer_get')
        dealer = json_result[0]
        
        dealer_obj = CarDealer(
            address=dealer["address"], 
            city=dealer["city"], 
            full_name=dealer["full_name"],
            id=dealer["id"], 
            lat=dealer["lat"], 
            long=dealer["long"],
            short_name=dealer["short_name"],
            st=dealer["st"], 
            zip=dealer["zip"]
        )
    return dealer_obj


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, api_key=None, dealer_id=dealer_id)
    if isinstance(json_result, list):
        reviews = json_result
        # Print or log the reviews for debugging
        print(reviews)
        # For each dealer object
        for review in reviews:
            # Get its content 
            review_obj = DealerReview(
                dealership=review.get("dealership", ""),
                name=review.get("name", ""),
                purchase=review.get("purchase", ""),
                review=review.get("review", ""),
                purchase_date=review.get("purchase_date", ""),               
                car_make=review.get("car_make", ""),
                car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""),
                sentiment='',
                id=review.get("id", "")
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
           

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    API_KEY = 'bGzxfI_dfm53PLexIyD2rBMlLwLy1r5s1fEOLgvRd0g4'
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/9de934ca-8c19-41c3-9897-0fb787b8b736'

    params = {
        "text": dealerreview,
        "version": "2022-04-07",  
        "features": "sentiment", 
        "return_analyzed_text": True
    }

    try:
        print('##################')
        response = get_request(url=NLU_URL, api_key=API_KEY, **params)
        sentiment = response.get('sentiment', {}).get('document', {}).get('label')
        print('##################')
        print(response)
        print('##################')
        print('##################')
        print(sentiment)
        print('##################')
        return sentiment
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None
