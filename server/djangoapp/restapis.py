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
import json
import requests

def post_request(url, json_payload, **kwargs):
    print("POST to {} ".format(url))
    
    # Use the 'json' parameter to send JSON data
    response = requests.post(
        url,
        params=kwargs,
        json=json_payload,  # Use 'json' parameter for JSON data
        headers={'Content-Type': 'application/json'},
    )

    status_code = response.status_code
    print("With status {} ".format(status_code))
    print("Response text: ", response.text)

    try:
        json_data = response.json()  # Use .json() to parse JSON response
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
def get_dealer_reviews_from_cf(url, id):
    results = []
    json_result = get_request(url, id=id)
    print(json_result) 

    if isinstance(json_result, list):
        for review in json_result:
            if review['purchase']:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=review['purchase_date'], 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=review['car_make'], 
                    car_model=review['car_model'], 
                    car_year=review['car_year'], 
                    id=review['id'], 
                    sentiment='sentiment'
                )
            else:
                review_obj = DealerReview(
                    dealership=review['dealership'], 
                    purchase=review['purchase'], 
                    purchase_date=None, 
                    name=review['name'], 
                    review=review['review'], 
                    car_make=None, 
                    car_model=None, 
                    car_year=None, 
                    id=review['id'], 
                    sentiment='sentiment'
                )
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
            print("Sentiments: ", review_obj.sentiment)
            print("Results: ", review_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    api_key = 'bGzxfI_dfm53PLexIyD2rBMlLwLy1r5s1fEOLgvRd0g4'
    url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/9de934ca-8c19-41c3-9897-0fb787b8b736'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=dealerreview+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[dealerreview+"hello hello hello"]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']

    return(label)

