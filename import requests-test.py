import requests
import numpy as np 
import json
import pandas as pd


def get_player_info():
    player_input = input("Ange id: ")
    playerId = player_input

    cols = ['id','fullName','birthDate','birthCity','birthCountry','shootsCatches','position','teamId','team','birthStateProvince']

    url = 'https://statsapi.web.nhl.com/api/v1/people/{}'.format(str(playerId))
    resp = requests.get(url=url)
    playerInfoJSON = json.loads(resp.text)

    playerInfo = pd.DataFrame(np.nan, range(0,1), columns = cols)
    playerInfo['id'] = playerId

    for i in range(1,len(cols)-4):
        playerInfo[cols[i]] = playerInfoJSON['people'][0][cols[i]]

    playerInfo['position'] = playerInfoJSON['people'][0]['primaryPosition']['code']
    if playerInfoJSON['people'][0]['active'] is False:
        playerInfo['teamId'] = np.nan   
        playerInfo['team'] = np.nan
    else:
        playerInfo['teamId'] = playerInfoJSON['people'][0]['currentTeam']['id']   
        playerInfo['team'] = playerInfoJSON['people'][0]['currentTeam']['name']

    NA = ['USA','CAN']

    if playerInfo.birthCountry[0] in NA:
        playerInfo['birthStateProvince'] = playerInfoJSON['people'][0]['birthStateProvince']

    print(playerInfo)


get_player_info()

