import requests
import json

def test():
    # Enter Team Id and Season Number (ex if season 2020-2021, enter 20202021)
    team_input = input("Enter a valid team: ")
    season_input = input("Enter a valid season (yyyyyyyy): ")

    # Request
    url = "https://statsapi.web.nhl.com/api/v1/teams/" + str(team_input) + "?expand=team.roster&season=" + season_input
    response = requests.get(url)
    data = response.json()

    data = data['teams'][0]['roster']['roster']

    team = {}

    for i in data:
        playerId = i['person']["id"]
        playerName = i['person']['fullName']
        team[playerName] = playerId

    stats = {"Name": ["Goals", "Assists", "Points"]}

    for i in team:
        leaf = team[i]
        r = requests.get('https://statsapi.web.nhl.com/api/v1/people/' + str(leaf) + '/stats?stats=statsSingleSeason&season=' + season_input)
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

        # "Fine" print of received data 
        print(json.dumps(stats, indent=1, sort_keys=True))


# Run func 
test()