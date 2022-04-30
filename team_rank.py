import requests
import json
import database
from datetime import date

"""
    Funktionen hämtar lagstatistik från nhl:s API och sparar i en lista av lexikon. 
"""

def get_team_rank():
    response_API=requests.get("https://statsapi.web.nhl.com/api/v1/standings")
    data = response_API.text
    json.loads(data) 
    parse_json=json.loads(data)

    

    all_teams=[]

    for team_records in parse_json["records"]:
        
        for element in team_records["teamRecords"]:
            team_name=element["team"]["name"]
            team_id=element["team"]["id"]
            
            team_wins=element["leagueRecord"]["wins"]
            team_losses=element["leagueRecord"]["losses"]
            team_ot=element["leagueRecord"]["ot"]

            team_points=element["points"]
            team_games_played=element["gamesPlayed"]

            team_loggo="https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + str(team_id) + ".svg"
            todaydate = date.today()

            all_teams.append({"teamName": team_name, "teamLoggo": team_loggo, "gamesPlayed":team_games_played, "wines":team_wins, "losses": team_losses, "ot":team_ot, "points":team_points, "timestamp":todaydate})

    database.insert_team_rank(all_teams)