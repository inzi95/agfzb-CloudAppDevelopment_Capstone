import requests
import json
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import NaturalLanguageUnderstandingV1, Features, SentimentOptions
from djangoapp.models import DealerReview, CarDealer

# from .models import CarDealer, DealerReview


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print(f"GET from {url}")
    try:
        response = requests.get(url,
                                params=kwargs,
                                headers={
                                    'Content-Type': 'application/json'},
                                )
    except:
        return "Network exception has occured."

    status_code = response.status_code
    print(f"With status {status_code}")
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


def post_request(url, **kwargs):
    response = requests.post(url, params=kwargs, json=kwargs['json'])
    return response.json()

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


def get_dealers_from_cf(url, **kwargs):

    results = []
    json_result = get_request(url, **kwargs)

    if json_result:
        dealers = json_result['body']['rows']
        for dealer in dealers:
            dealer_doc = dealer['doc']
            dealer_obj = CarDealer(address=dealer_doc['address'],
                                   city=dealer_doc['city'],
                                   full_name=dealer_doc['full_name'],
                                   id=dealer_doc['id'],
                                   short_name=dealer_doc['short_name'],
                                   st=dealer_doc['st'],
                                   zip=dealer_doc['zip'],
                                   long=dealer_doc['long'],
                                   lat=dealer_doc['lat'],
                                   )
            results.append(dealer_obj)

        return results
    else:
        return {
            "StatusCode": 500,
            "message": "Something has gone wrong in retrieving the results."
        }

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list


def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url, **kwargs)
    if json_result:
        reviews = json_result['body']['data']['docs']
        for review in reviews:
            review_doc = review
            if review_doc['purchase'] == False:
                review_doc['purchase_date'] = ""
                review_doc['car_make'] = ""
                review_doc['car_model'] = ""
                review_doc['car_year'] = ""

            review_obj = DealerReview(dealership=review_doc['dealership'],
                                      name=review_doc['name'],
                                      review=review_doc['review'],
                                      purchase=review_doc['purchase'],
                                      purchase_date=review_doc['purchase_date'],
                                      car_make=review_doc['car_make'],
                                      car_model=review_doc['car_model'],
                                      car_year=review_doc['car_year'],
                                      #   id=review_doc['id'],
                                      sentiment=analyze_review_sentiments(
                                          review_doc['review']),
                                      )
            results.append(review_obj)
        return results
    else:
        return {
            "statusCode": 500,
            "message": "Something had gone wrong!"
        }


def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/ea2716e8-9754-48b5-9e06-43c342a243f8"
    api_key = "Ebn9Ed5n7QnA_k2BMBGofcXdaoIN2QxdChLZQ7HJJ678"
    authenticator = IAMAuthenticator(api_key)

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01', authenticator=authenticator)

    natural_language_understanding.set_service_url(url)

    response = natural_language_understanding.analyze(language='en', text=text, features=Features(
        sentiment=SentimentOptions(targets=[text]))).get_result()

    label = json.dumps(response, indent=2)

    label = response['sentiment']['document']['label']

    return(label)
