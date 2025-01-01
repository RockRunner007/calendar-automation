
# https://developers.strava.com/docs/getting-started/
# https://www.strava.com/settings/api
# Authorization: Bearer #{access_token}

# curl -X POST https://www.strava.com/oauth/token \
# 	-F client_id=YOURCLIENTID \
# 	-F client_secret=YOURCLIENTSECRET \
# 	-F code=AUTHORIZATIONCODE \
# 	-F grant_type=authorization_code

# APP_SETTINGS=settings.cfg python3 server.py
# example: https://github.com/Cloudy17g35/strava-api/blob/main/main.py

import requests
import json
from stravalib.client import Client

my_client_id=0
my_client_secret=""

client = Client()
authorize_url = client.authorization_url(
    client_id=my_client_id, redirect_uri="http://localhost:8282/authorized"
)

code = requests.get("code")  # or whatever your framework does
token_response = client.exchange_code_for_token(
    client_id=my_client_id, client_secret=my_client_secret, code=code
)
access_token = token_response["access_token"]
refresh_token = token_response["refresh_token"]
expires_at = token_response["expires_at"]

# Now store that short-lived access token somewhere (a database?)
client.access_token = access_token
# You must also store the refresh token to be used later on to obtain another valid access token
# in case the current is already expired
client.refresh_token = refresh_token

# An access_token is only valid for 6 hours, store expires_at somewhere and
# check it before making an API call.
client.token_expires_at = expires_at

athlete = client.get_athlete()
print(
    "For {id}, I now have an access token {token}".format(
        id=athlete.id, token=access_token
    )
)

