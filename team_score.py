import database
import player_info

def count_difference ():
    players_API_list=player_info.get_all_players_API()
    players_database_list=database.get_all_players()
    score_list=[]

    for person in players_API_list:
        person_goal=person["goal"]
        person_penelty_time=person["penalty_time"]
        person_assists=person["assists"]
        person_saves=person["saves"]
       

        for player in players_database_list:
            player_id=player["id"]

            if person["id"]==player_id:
                player_goal=player["goal"]
                player_penalty_time=player["penalty_time"]
                player_assists=player["assists"]
                player_saves=player["saves"]
               

                goal_score= (int(person_goal) - int(player_goal)) * 2
                penalty_time_score= round(int(person_penelty_time) - int(player_penalty_time))
                assists_score= int(person_assists) - int(player_assists) 
                saves_score= int(person_saves) - int(player_saves)

                all_score = goal_score + penalty_time_score + assists_score + saves_score

                score_list.append({"id":player_id, "score":all_score})
        return score_list
    
def insert_score_to_database():
    player_score_list=count_difference()
    fhl_user_team_list=database.get_team_list_fhl_team()
    print(fhl_user_team_list)

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

        database.insert_team_score(team_score, team_id)

insert_score_to_database()