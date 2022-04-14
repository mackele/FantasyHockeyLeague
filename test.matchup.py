import requests
import numpy as np 
import json
import pandas as pd
import math

def get():
    # make input 
    playerid = "8479291"
    seasonid = "20202021"
    team_input = "10"

    # Request
    url = "https://statsapi.web.nhl.com/api/v1/teams/" + str(team_input) + "?expand=team.roster&season=" + seasonid
    response = requests.get(url)
    data = response.json()

    data = data['teams'][0]['roster']['roster']

    team = {}

    var = []

    for i in data:
        playerId = i['person']["id"]
        playerName = i['person']['fullName']
        team[playerName] = playerId

    stats = {"Name": ["Goals", "Assists", "Points"]}

    for i in team:
        leaf = team[i]
        r = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(leaf) + '/stats?stats=statsSingleSeason&season=' + seasonid)
        data = json.loads(r.text)

        # Checks if there is points or assists, won't include players without points (rookies, goalies, etc)
        if len(data['stats'][0]['splits']) > 0:
            try:
                goals = data['stats'][0]['splits'][0]['stat']['goals']
            except:
                goals = 0
            try:
                assists = data['stats'][0]['splits'][0]['stat']['assists']
            except:
                assists = 0
            try:
                points = data['stats'][0]['splits'][0]['stat']['points']
            except:
                points = 0
            stats[i] = [goals, assists, points]
        else:
            stats[i] = [0, 0, 0]

        var.append(stats[i])

    print(var)


get()