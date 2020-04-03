# Crowdstrike_python_example
Simple example on how to authenticate and call Crowdstrike oauth2 apis

I made this script because I couldn't find a simple example on how to call Crowdstrike in python and thought since I worked it out I would share.  

###################################################################################################
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
