##################################################################################################
# 20200403 - Chooka888
# This script is a simple example showing how to authenticate to and call Crowdstrike's Oauth2 APIs.
# Details of the API can be found in Crowdstrike Docs and https://assets.falcon.crowdstrike.com/support/api/swagger.html#
# 
# Example flows is made up of 3 sections:
#   1. Authenticate by posting a Crowdstrike API Client ID and Client Secret to the authentication URL - https://api.crowdstrike.com/oauth2/token
#   2. Capturing the authentication token from the response
#   3. Calling the IoC search domain API and including the bearer authentication token as a "authorization" header
#
# NOTE you may need to install the requests and json libraries. 
#
###################################################################################################

import requests
import json

# Define API REST paths
BASE_URL = "https://api.crowdstrike.com/"
OAUTH_URL_PART = "oauth2/token"
IOC_DEVICE_SEARCH = "indicators/queries/devices/v1"

# Empty auth token to hold value for subsequent request
auth_Token = ""

# Section 1 - Authenticate to Crowdstrike OAUTH

# Build a dictionary to hold the headers
headers = {
    'Content-type': 'application/x-www-form-urlencoded', 
    'accept': 'application/json'
}

# Build a dictionary to holds the authentication data to be posted to get a token
auth_creds = {}
auth_creds['client_id'] = "<Your Client Id>"
auth_creds['client_secret'] = "<Your Client Secret>"
auth_creds['grant_type'] = "client_credentials"

# Call the API to get a Authentication token - NOTE the authentication creds 
print("Requesting token from " + BASE_URL + OAUTH_URL_PART)
auth_response = requests.post(BASE_URL + OAUTH_URL_PART,data=auth_creds, headers=headers)

# Check if successful
if auth_response.status_code != 201:
    # Output debug information
    print("\n Return Code: " + str(auth_response.status_code) + " " + auth_response.reason)
    print("Path: " + auth_response.request.path_url)
    print("Headers: ")
    print(auth_response.request.headers)
    print("Body: " + auth_response.request.body)
    print("\n")
    print("Trace_ID: " + auth_response.json()['meta']['trace_id'])
else:

    # Section 2 - Capture OAUTH token and store in headers for later use

    print("Token Created")
    # Capture the auth token for reuse in subsequent calls, by pulling it from the response
    # Note this token can be reused multiple times until it expires after 30 mins
    auth_Token = auth_response.json()['access_token']
 
    headers = {
        'authorization':'bearer ' + auth_Token,
        'accept': 'application/json'
    }

# Section 3 - Reuse authentication token to call other Crowdstrike OAUTH2 APIs

# Build parameter dictionary
call_params = {}
call_params['type'] ="domain"
call_params['value'] ="crowdstrike.com"
call_params['limit'] ="" # Non-mandatory param
call_params['offset'] ="" # Non-mandatory param

# Call IoC devices API 
print("Searching IoC by getting from " + BASE_URL + IOC_DEVICE_SEARCH)
IoC_search_response = requests.get(BASE_URL + IOC_DEVICE_SEARCH,params=call_params,headers=headers)

# Check for errors
if IoC_search_response.status_code != 200:
    # Output debug information
    print("\n Return Code: " + str(IoC_search_response.status_code) + " " + IoC_search_response.reason)
    print("Path: " + IoC_search_response.request.path_url)
    print("Headers: ")
    print(IoC_search_response.request.headers)
    print("Body: " + IoC_search_response.request.body)
    print("\n")
    print("Trace_ID: " + IoC_search_response.json()['meta']['trace_id'])
else:
    # Iterate the results and print 
    result = IoC_search_response.json()
    print("IoC found on " + str(len(result['resources'])) + " the following device id:")
    for devices in result['resources']:
        print(devices)
