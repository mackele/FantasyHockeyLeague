import requests
import json
from database import *

def get_all_players():
    response_API=requests.get("https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster")
    data = response_API.text
    json.loads(data) 
    parse_json=json.loads(data)

    

    #all_players=[]
    goalies = []
    players = []

    for team in parse_json["teams"]:
        team_name=team["name"]
        roster=team["roster"]

        for person in roster["roster"]:
            person_name=person["person"]["fullName"]
            person_id=person["person"]["id"]
            position=person["position"]["name"]

            season="20202021"

            response=requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(person_id) + "/stats?stats=statsSingleSeason&season=" + str(season))

            info = response.text
            json.loads(info) 
            parse=json.loads(info)

            if position == "Goalie":
                for stats in parse["stats"]:
                    for splits in stats["splits"]:
                        saves=splits["stat"]["saves"]
                        price_goalie = round(int(saves) / 12)
                        goal_goalie = 0
                        penalty_time_goalie = 0
                        assists_goalie = 0
                        image_goalie = "Inget"
                        #Gjort lite ändringar så att det förs in i databasen i korrekt ordning
                        goalies.append({"id":person_id, "team": team_name, "position": position, "goal": goal_goalie, "penalty_time": penalty_time_goalie, "assists": assists_goalie, "image": image_goalie, "price": price_goalie, "saves": saves, "name": person_name})
                        

            if position !="Goalie":
                for stats in parse["stats"]:
                    for splits in stats["splits"]:
                        goals=splits["stat"]["goals"]
                        assists=splits["stat"]["assists"]
                        penalty_minutes=splits["stat"]["penaltyMinutes"]
                        price_player = round((int(goals) + int(assists)) - (int(penalty_minutes) / 4))
                        saves_player = 0
                        image_player = "Inget"
                        #Gjort lite ändringar så att det förs in i databasen i korrekt ordning
                        players.append({
                            "id": person_id,
                            "team": team_name,
                            "position": position,
                            "goal": goals,
                            "penalty_time": penalty_minutes,
                            "assists": assists,
                            "image": image_player,
                            "price": price_player,
                            "saves": saves_player,
                            "name": person_name                            
                        })

    

    #Funktioner som lägger till målvakter respektive spelare, bara att köra de enskilt för att mata in i databasen
    
    #add_goalie_to_database(goalies)  
    #add_player_to_database(players)         
             
get_all_players()

#Tar ca 2 min att köra, allt syns inte i vsc men laddas (Allt syns i kommandotolken). 853 personer

#Kolla tabellen i databasen innan detta insertas där.
