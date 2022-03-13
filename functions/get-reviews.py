from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(params):
    authenticator = IAMAuthenticator('dq4ca8I5OZmoM1Grn4HrIz2-RTUMIwepfgj57RM8fpJW')
    
    service = CloudantV1(authenticator=authenticator)
    
    service.set_service_url("https://apikey-v2-9rn99dhfn3u2imxotbzqxwal0s2tpn46i3lb7wqim2f:d12bf06325b4f71100cba764082e9c08@2eea836a-90fd-4b86-8646-8cc9f19c0f91-bluemix.cloudantnosqldb.appdomain.cloud")
    
    response = service.post_find(
    db='reviews',
    selector={'dealership': {'$eq': int(params['id'])}},
    ).get_result()
    
    try:
        # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
            'statusCode':404,
            'message':"Something went wrong!"
        }