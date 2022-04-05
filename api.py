#import libraries
from http import client
import requests
import time
import json

#SHL inlogg
#Klient-ID: 0727233fb0228d3e8b4fd4c972610210
#Lösen: 9301628f4d7101d44389e04e63f17d93183a86087dda5722bdc8a7ed366e8934



#Hämtar information i JSON format från NHLs API
#response = requests.get("http://statsapi.web.nhl.com/api/v1/people/8471214?hydrate=stats%28splits%3DstatsSingleSeason%29").json()
#print(response)

#Har inte förstått hur man gör med SHLs API än
API_ENDPOINT = 'openapi.shl.se'
Client_id = '0727233fb0228d3e8b4fd4c972610210'
Client_secret = '9301628f4d7101d44389e04e63f17d93183a86087dda5722bdc8a7ed366e8934'
REDIRECT_URI = 'google.se'

def exchange_code(code):
    data = {
        'client_id': Client_id,
        'client_secret': Client_secret,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    r = requests.post(API_ENDPOINT + '/ouath2/token', data=data, headers=headers)
    r.raise_for_status()
    return r.json()

#token = exchange_code('https://openapi.shl.se/oauth2/token')
exchange_code('open-shl')