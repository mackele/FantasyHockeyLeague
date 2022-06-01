from tkinter import N
import requests
import json
import database
from datetime import date
from datetime import datetime 
import pytz 

# Emilia 
def get_play_schedual ():
    '''
        funktionen körs från fhl.py

        Funktionen hämtar data från nhl:s api utifrån dagens datum. 
        Tiden som hämtas ut ändras till sveriges tidszon och delas upp i datum och tid.
        Lagens loggor hämtas ut utifrån lagens id.
        Allt sparas i en lista med lexikon. 
        Listan skickas till funktionen insert_play_schedual i filen database.py. 
    '''
    todaydate = date.today()
    response_API=requests.get("https://statsapi.web.nhl.com/api/v1/schedule?startDate=" + str(todaydate) + "&endDate=" + str(todaydate))
    
    data = response_API.text
    json.loads(data) 
    parse_json=json.loads(data)

    timezone = 'Europe/Stockholm'
    local_tz = pytz.timezone(timezone)

    current_days_games=[]

    for play in parse_json["dates"]:

        for team in play["games"]:
            game_date_time=team["gameDate"]
            time= datetime.fromisoformat(game_date_time[:-1])

            
            local_dt = time.replace(tzinfo=pytz.utc).astimezone(local_tz)
            game_play_local_timezone = local_tz.normalize(local_dt)
            game_play_date=game_play_local_timezone.strftime("%Y-%m-%d")
            game_play_time=game_play_local_timezone.strftime("%H:%M")

            team_away_name=team["teams"]["away"]["team"]["name"]
            team_away_id=team["teams"]["away"]["team"]["id"]
            team_away_loggo="https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + str(team_away_id) + ".svg"

            team_home_name=team["teams"]["home"]["team"]["name"]
            team_home_id=team["teams"]["home"]["team"]["id"]
            team_home_loggo="https://www-league.nhlstatic.com/images/logos/teams-current-primary-light/" + str(team_home_id) + ".svg"

            current_days_games.append({"team_away_name":team_away_name, "team_away_loggo": team_away_loggo, "game_date": game_play_date, "game_time":game_play_time, "team_home_name":team_home_name, "team_home_loggo": team_home_loggo})
    
    database.insert_play_schedual(current_days_games)
            