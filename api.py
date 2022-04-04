#import libraries
from http import client
import requests
import time
import json

#SHL inlogg
#Klient-ID: 0727233fb0228d3e8b4fd4c972610210
#Lösen: 9301628f4d7101d44389e04e63f17d93183a86087dda5722bdc8a7ed366e8934



#Hämtar information i JSON format från NHLs API
response = requests.get("http://statsapi.web.nhl.com/api/v1/people/8471214?hydrate=stats%28splits%3DstatsSingleSeason%29").json()
print(response)

#Har inte förstått hur man gör med SHLs API än