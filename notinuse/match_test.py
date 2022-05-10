import json 
import requests 

def request(url):
        response = requests.get(url)
        data = response.json()
        print(json.dumps(data, indent=1, sort_keys=True))

def get_data_for_rangers(): 

    team_input = input("Enter an active player in New York Rangers: ")

    if team_input == "Sammy Blais":
        url = "https://statsapi.web.nhl.com/api/v1/people/8478104"
        request(url)

    elif team_input == "Kevin Rooney":
        url = "https://statsapi.web.nhl.com/api/v1/people/8479291"
        request(url)

    elif team_input == "Kaapo Kakko":
        url = "https://statsapi.web.nhl.com/api/v1/people/8481554"
        request(url)

    elif team_input == "Ryan Reaves":
        url = "https://statsapi.web.nhl.com/api/v1/people/8471817"
        request(url)

    elif team_input == "Justin Braun":
        url = "https://statsapi.web.nhl.com/api/v1/people/8474027"
        request(url)

    elif team_input == "Chris Kreider":
        url = "https://statsapi.web.nhl.com/api/v1/people/8475184"
        request(url)

    elif team_input == "Greg McKegg":
        url = "https://statsapi.web.nhl.com/api/v1/people/8475735"
        request(url)

    elif team_input == "Patrik Nemeth":
        url = "https://statsapi.web.nhl.com/api/v1/people/8475747"
        request(url)

    elif team_input == "Ryan Strome":
        url = "https://statsapi.web.nhl.com/api/v1/people/8476458"
        request(url)

    elif team_input == "Barclay Goodrow":
        url = "https://statsapi.web.nhl.com/api/v1/people/8476624"
        request(url)

    elif team_input == "Jacob Trouba":
        url = "https://statsapi.web.nhl.com/api/v1/people/8476885"
        request(url)
        
    elif team_input == "Tyler Motte":
        url = "https://statsapi.web.nhl.com/api/v1/people/8477353"
        request(url)
        
    elif team_input == "Jonny Brodzinski":
        url = "https://statsapi.web.nhl.com/api/v1/people/8477380"
        request(url)
        
    elif team_input == "Andrew Copp":
        url = "https://statsapi.web.nhl.com/api/v1/people/8477429"
        request(url)
        
    elif team_input == "Igor Shesterkin":
        url = "https://statsapi.web.nhl.com/api/v1/people/8478048"
        request(url)
        
    elif team_input == "Dryden Hunt":
        url = "https://statsapi.web.nhl.com/api/v1/people/8478211"
        request(url)
        
    elif team_input == "Frank Vatrano":
        url = "https://statsapi.web.nhl.com/api/v1/people/8478366"
        request(url)
        
    elif team_input == "Artemi Panarin":
        url = "https://statsapi.web.nhl.com/api/v1/people/8478550"
        request(url)
        
    elif team_input == "Adam Fox":
        url = "https://statsapi.web.nhl.com/api/v1/people/8479323"
        request(url)

    elif team_input == "Ryan Lindgren":
        url = "https://statsapi.web.nhl.com/api/v1/people/8479324"
        request(url)

    elif team_input == "Julien Gauthier":
        url = "https://statsapi.web.nhl.com/api/v1/people/8479328"
        request(url)

    elif team_input == "Libor Hajek":
        url = "https://statsapi.web.nhl.com/api/v1/people/8479333"
        request(url)

    elif team_input == "Filip Chytil":
        url = "https://statsapi.web.nhl.com/api/v1/people/8480078"
        request(url)

    elif team_input == "Alexandar Georgiev":
        url = "https://statsapi.web.nhl.com/api/v1/people/8480382"
        request(url)

    elif team_input == "K'andre Miller":
        url = "https://statsapi.web.nhl.com/api/v1/people/8480817"
        request(url)

    elif team_input == "Braden Schneider":
        url = "https://statsapi.web.nhl.com/api/v1/people/8482073"
        request(url)

    elif team_input == "Alexis Lafreniere":
        url = "https://statsapi.web.nhl.com/api/v1/people/8482109"
        request(url)

    elif team_input == "Mika Zibanejad":
        url = "https://statsapi.web.nhl.com/api/v1/people/8476459/stats?stats=statsSingleSeason&season=20202021"
        url1 = "https://statsapi.web.nhl.com/api/v1/people/8476459"
        request(url)
        request(url1)
    else:
        print("Player does not exist")

def run_teams():
    get_data_for_rangers()

run_teams()
