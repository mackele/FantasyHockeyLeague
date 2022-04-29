import requests
import json

def get_all_players():
    response_API=requests.get("https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster")
    data = response_API.text
    json.loads(data) 
    parse_json=json.loads(data)

    

    all_players=[]

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
                        all_players.append({"person_name":person_name, "person_id":person_id, "team_name": team_name, "position": position, "saves":saves})
                        

            if position !="Goalie":
                for stats in parse["stats"]:
                    for splits in stats["splits"]:
                        goals=splits["stat"]["goals"]
                        assists=splits["stat"]["assists"]
                        penalty_minutes=splits["stat"]["penaltyMinutes"]
                        all_players.append({"person_name":person_name, "person_id":person_id, "team_name": team_name, "position": position, "goals": goals, "assists":assists, "penalty_minutes": penalty_minutes})

    print(all_players)           
             
get_all_players()

#Tar ca 2 min att köra, allt syns inte i vsc men laddas (Allt syns i kommandotolken). 853 personer

#Kolla tabellen i databasen innan detta insertas där.
