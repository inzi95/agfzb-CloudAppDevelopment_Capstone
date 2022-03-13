from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):
    authenticator = IAMAuthenticator('dq4ca8I5OZmoM1Grn4HrIz2-RTUMIwepfgj57RM8fpJW')
    
    client = CloudantV1(authenticator=authenticator)
    
    client.set_service_url("https://apikey-v2-9rn99dhfn3u2imxotbzqxwal0s2tpn46i3lb7wqim2f:d12bf06325b4f71100cba764082e9c08@2eea836a-90fd-4b86-8646-8cc9f19c0f91-bluemix.cloudantnosqldb.appdomain.cloud")
    

    jsonDocument = {
    "name": params['name'],
    "dealership": params['dealership'],
    "review": params['review'],
    "purchase": params['purchase'],
    "purchase_date": params['purchase_date'],
    "car_make": params['car_make'],
    "car_model": params['car_model'],
    "car_year": params['car_year']
    }

    try:
        create_doc = client.post_document(db='reviews', document=jsonDocument)
        response = client.post_find(
        db='reviews',
        selector={'dealership': {'$eq': int(params['dealership'])}},
        ).get_result()
        return response
    
    except:
        return {
        "statusCode": 404,
        "message": "Something went wrong with the server"
        }
