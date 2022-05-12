import database
import player_info

players_API_list=player_info.get_all_players_API()
players_database_list=database.get_all_players()

def count_difference ():
    """
        Funktionen jämför spelarnas statistik i NHL:s API från dagens datum med spelarnas statistik i databasen som inte är dagens datum.

        Return:
            Returnerar en lista med lexikon med spelarnas id samt deras sammanlagda skillnader i statistiken.
    """
    score_list=[]

    for player in players_database_list:
        player_id=player["id"]
        player_goal=player["goal"]
        player_penalty_time=player["penalty_time"]
        player_assists=player["assists"]
        player_saves=player["saves"]

        for person in players_API_list:
            person_id=person["id"]
            if person_id==player_id: 
                person_goal=person["goal"]
                person_penelty_time=person["penalty_time"]
                person_assists=person["assists"]
                person_saves=person["saves"]
                       
                print(player_saves, person_saves)

                goal_score= (person_goal - player_goal) * 2
                penalty_time_score= round(int(person_penelty_time) - int(player_penalty_time))
                assists_score= person_assists - player_assists 
                saves_score= person_saves - player_saves
                all_score = (goal_score + penalty_time_score + assists_score + saves_score)

                score_list.append({"id":player_id, "score":all_score})
    
    print(score_list)
    return score_list

def delete_players ():
    '''
        Funktionen kör funktionen delete_players_in_database i databas.py. 
    '''
    database.delete_players_in_database()

def insert_players_to_database(players_API_list):
    """
        Funktionen kör funktionen add_player_to_database i filen databas.py.
        args:
            Listan med lexikon med spelarna och deras statistik som hämtats från NHL:s API. Listan skickas mer till databas.py
    """
    database.add_player_to_database(players_API_list)

def insert_score_to_database():
    """
        Funktionen hämtar ut en lista med de lagda lagen i databasen som inte har någon poäng än. 
        Lagets poäng räknas ut beroende på vilka spelare som finns i laget och den sammanlagda skillnaden som tagits ut i funktionen count_difference.
        Poängen skickas in till databasen baserat på lagets id.
        Spelarna i databasen raderas och läggs in på nytt med ny statistik.
    """

    player_score_list=count_difference()
    fhl_user_team_list=database.get_team_list_fhl_team()

    for team in fhl_user_team_list:
        first_player_id=team[2]
        second_player_id=team[3]
        third_player_id=team[4]
        fourth_player_id=team[5]
        fifth_player_id=team[6]
        sixth_player_id=team[7]

        team_id=team[9]
        
        team_score= 0

        for player in player_score_list:
            if player["id"]==first_player_id or player["id"]==second_player_id or player["id"] == third_player_id or player["id"]==fourth_player_id or player["id"]==fifth_player_id or player["id"]==sixth_player_id:
                team_score = team_score + int(player["score"])
        print(team_score, team_id)
        database.insert_team_score(team_score, team_id)
   
    delete_players ()
    insert_players_to_database(players_API_list)   
