import requests
import json
from .models import CarMake, CarModel, CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if 'api' in kwargs:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                     auth=HTTPBasicAuth('apikey', api_key))
            print(response,'api')
        elif kwargs:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'}, params=kwargs)
            print(params,"second")
        else:
            response = requests.get(
                url, headers={'Content-Type': 'application/json'})
            print('third')

    except Exception as e:
        
        print("Network exception occurred")
        
    status_code=response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    
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

    # def get_dealers_from_cf(url, **kwargs):
    # results = []
    # # Call get_request with a URL parameter
    # json_result = get_request(url)
    # if json_result:
    #     # Get the row list in JSON as dealers
    #     dealers = json_result["rows"]
    #     # For each dealer object
    #     for dealer in dealers:
    #         # Get its content in `doc` object
    #         dealer_doc = dealer["doc"]
    #         # Create a CarDealer object with values in `doc` object
    #         dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
    #                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
    #                                short_name=dealer_doc["short_name"],
    #                                st=dealer_doc["st"], zip=dealer_doc["zip"])
    #         results.append(dealer_obj)

    # return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=kwargs["dealerId"])
    
    if isinstance(json_result, list):
        reviews = json_result
        # Print or log the reviews for debugging
        print(reviews)
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
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
def analyze_review_sentiments(dealer_review):
    API_KEY = "bGzxfI_dfm53PLexIyD2rBMlLwLy1r5s1fEOLgvRd0g4"
    NLU_URL = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/9de934ca-8c19-41c3-9897-0fb787b8b736'
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)
    natural_language_understanding.set_service_url(NLU_URL)
    response = natural_language_understanding.analyze(text=dealer_review,language='en', features=Features(
        sentiment=SentimentOptions(targets=[dealer_review]))).get_result()
    label = json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)

