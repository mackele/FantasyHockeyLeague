import psycopg2
import sys 
from datetime import date
from datetime import datetime
from connect import Postgres
from flask import Flask, render_template, redirect, url_for, request, redirect #behövs denna?
from psycopg2.extras import execute_values


# Emilia 
def get_timestamp_fhl_players(todays_date):
    '''
        Funktionen hämtar datumet från tabellen fhl_players som finns i databasen.

        args:
            syftar till dagens datum som skickas med från fhl.py
        return:
            returnerar en lista med resultatet från sökningen i databasen till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select insert_date
                            from fhl_players
                                where insert_date=%s 
                                    limit 1""",
                                (todays_date,))
        list = cursor.fetchall()
    
    return list   


# Marcus 
def add_player_to_database(players):
    '''
    Funktion som lägger in spelare som hämtas i en lista med lexikon från APIn i player_info.py
    '''

    for player in players:
        player_id=player["id"]
        player_team=player["team"]
        player_position=player["position"]
        player_goal=player["goal"]
        player_penalty_time=player["penalty_time"]
        player_assists=player["assists"]
        player_image=player["image"]
        player_price=player["price"]
        player_saves=player["saves"]
        insert_date=player["date"]

        with Postgres() as (cursor, conn):
            PostgreSQL_insert = (f""" update fhl_players
                                    set team = '{player_team}',
                                     position = '{player_position}',
                                     goal = {player_goal},
                                     penalty_time = {player_penalty_time},
                                     assists = {player_assists},
                                     image = '{player_image}',
                                     price = {player_price},
                                     saves = {player_saves},
                                     insert_date= '{insert_date}'
                                        where id ={player_id};""")
            
            cursor.execute(PostgreSQL_insert)
            conn.commit()


# Emilia 
def search(user_search, user_id):

    '''
        Funktionen hämtar ut användarens sökning från databasen. Datan jämförs med listan med användarens köpta spelare och tar bort dessa från söklistan. 

        args:
            user_serch är den variabel som skickas med i sökningen för att hitta det användaren söker efter.
        
        return:
            Funktionen returnerar listan med de spelare som matchar med sökningen användaren gjorde. 
    '''

    with Postgres() as (cursor, conn):
       
        cursor.execute("""select *
                            from fhl_players
                                where name like %s""",
                                ('%' + user_search + '%',))
        all_players = cursor.fetchall()

        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' """)
        my_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]

                if player_id==person_id:
                    del players[i]

    return players
    


# Marcus 
def add_players_to_list(info):
    '''
    Funktion som tar SQL frågan (info) och sedan tar denna och sorterar den i en lista av lexikon
    som sedan läggs till i en tom lista och skickas tillbaka

    Return: players 
    Som är alla de spelare som fanns i SQL-frågan sorterade i en ny lista av lexikon
    '''

    players = []

    for list in info:
        id = list[0]
        name = list[9]
        team = list[1]
        position = list[2]
        goal = list[3]
        penalty_time = list[4]
        assists = list[5]
        image = list[6]
        price = list[7]
        saves = list[8]

        players.append({
            "id": id,
            "name": name,
            "team": team,
            "position": position,
            "goal": goal,
            "penalty_time": penalty_time,
            "assists": assists,
            "image": image,
            "price": price,
            "saves": saves
        }) 

    return players           


# Marcus 
def get_all_players():
    """
    Funktion som hämtar alla spelare till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


# Marcus, Emilia
def get_center_players(user_id):
    """
        Funktion som hämtar alla center spelare som inte är köpta av användaren till en lista av lexikon som sedan används i fhl.py för att printa ut 
        spelarkort.

        args:
            user_id är användarens mail och används för hämta ut användarens köpta spelare och ta bort dessa i listan

        Returns: center_players
            Detta är en lista av lexikon med de icke köpta spelarna
        """
    
    with Postgres() as (cursor, conn):
        
        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' and fhl_players.position = 'Center' """)
        my_players=cursor.fetchall()

        
            
        cursor.execute (f"""select * from fhl_players
                        where position = 'Center' order by price desc """)
        all_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]
                if player_id==person_id:
                    del players[i]

    return players


# Marcus, Emilia
def get_right_forward_players(user_id):
    """
        Funktion som hämtar alla höger forward spelare som inte är köpta av användaren till en lista av lexikon som sedan används i fhl.py för att printa ut 
        spelarkort.

        args:
            user_id är användarens mail och används för hämta ut användarens köpta spelare och ta bort dessa i listan

        Returns: center_players
            Detta är en lista av lexikon med de icke köpta spelarna
    """
    with Postgres() as (cursor, conn):
        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' and fhl_players.position = 'Right Wing' """)
        my_players=cursor.fetchall()

        cursor.execute ("""select * from fhl_players where position = 'Right Wing' order by price desc""")
        all_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]
                if player_id==person_id:
                    del players[i]

    return players


# Marcus, Emilia
def get_left_forward_players(user_id):
    """
        Funktion som hämtar alla vänster forward spelare som inte är köpta av användaren till en lista av lexikon som sedan används i fhl.py för att printa ut 
        spelarkort.

        args:
            user_id är användarens mail och används för hämta ut användarens köpta spelare och ta bort dessa i listan

        Returns: center_players
            Detta är en lista av lexikon med de icke köpta spelarna
    """
    with Postgres() as (cursor, conn):
        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' and fhl_players.position = 'Left Wing' """)
        my_players=cursor.fetchall()

        cursor.execute ("""select * from fhl_players where position = 'Left Wing' order by price desc""")
        all_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]
                if player_id==person_id:
                    del players[i]

    return players


# Marcus, Emilia
def get_defense_players(user_id):
    """
        Funktion som hämtar alla backar spelare som inte är köpta av användaren till en lista av lexikon som sedan används i fhl.py för att printa ut 
        spelarkort.

        args:
            user_id är användarens mail och används för hämta ut användarens köpta spelare och ta bort dessa i listan

        Returns: center_players
            Detta är en lista av lexikon med de icke köpta spelarna
    """
    with Postgres() as (cursor, conn):

        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' and fhl_players.position = 'Defenseman' """)
        my_players=cursor.fetchall()

        cursor.execute ("""select * from fhl_players where position = 'Defenseman' order by price desc""")
        all_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]
                if player_id==person_id:
                    del players[i]

    return players


# Marcus, Emilia
def get_goalie_players(user_id):
    """
        Funktion som hämtar alla målvakter spelare som inte är köpta av användaren till en lista av lexikon som sedan används i fhl.py för att printa ut 
        spelarkort.

        args:
            user_id är användarens mail och används för hämta ut användarens köpta spelare och ta bort dessa i listan

        Returns: center_players
            Detta är en lista av lexikon med de icke köpta spelarna
    """
    with Postgres() as (cursor, conn):
        cursor.execute (f""" select * from fhl_players join fhl_my_players on fhl_my_players.player=fhl_players.id 
                            where fhl_my_players.fhl_user='{user_id}' and fhl_players.position = 'Goalie' """)
        my_players=cursor.fetchall()

        cursor.execute ("""select * from fhl_players where position = 'Goalie' order by price desc""")
        all_players=cursor.fetchall()

        players = add_players_to_list(all_players)

        for player in my_players:
            player_id=player[0]

            for i, person in enumerate(players):
                person_id=person["id"]
                if player_id==person_id:
                    del players[i]

    return players


# Lukas
def get_users_players(user_id):
    '''
        Funktion hämtar den inloggade användarens spelare
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players 
            as f join fhl_my_players as m on f.id = m.player 
                where m.fhl_user = %s""", (user_id,))
        info=cursor.fetchall()

        players = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            players.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
        

        return players


# Lukas
def get_users_goalie(user_id):
    '''
        Funktion hämtar den inloggade användarens målvakter
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and position = 'Goalie'""")
        info=cursor.fetchall()

        goalie = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            goalie.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return goalie


# Lukas
def get_users_defenseman(user_id):
    '''
        Funktion hämtar den inloggade användarens backar
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and position = 'Defenseman'""")
        info=cursor.fetchall()

        defenseman = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            defenseman.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return defenseman


# Lukas
def get_users_left_wing(user_id):
    '''
        Funktion hämtar den inloggade användarens vänsterforwards 
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and position = 'Left Wing'""")
        info=cursor.fetchall()

        left_wing = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            left_wing.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return left_wing


# Lukas
def get_users_center(user_id):
    '''
        Funktion hämtar den inloggade användarens centrar
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and position = 'Center'""")
        info=cursor.fetchall()

        center = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            center.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return center


# Lukas
def get_users_right_wing(user_id):
    '''
        Funktion hämtar den inloggade användarens högerforwards
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and position = 'Right Wing'""")
        info=cursor.fetchall()

        right_wing = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            right_wing.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return right_wing


# Lukas
def get_users_forward(user_id):
    '''
        Funktion hämtar den inloggade användarens forwards
        args:
            user_id är den inloggade användarens id
    '''

    with Postgres() as (cursor, conn):
        cursor.execute (f"""select * from fhl_players join fhl_my_players on fhl_players.id = fhl_my_players.player 
                where fhl_my_players.fhl_user = '{user_id}' and (position = 'Right Wing' or position = 'Left Wing')""")
        info=cursor.fetchall()

        forward = []

        for list in info:
            id = list[0]
            name = list[9]
            team = list[1]
            position = list[2]
            goal = list[3]
            penalty_time = list[4]
            assists = list[5]
            image = list[6]
            price = list[7]

            forward.append({
                "id": id,
                "name": name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "image": image,
                "price": price
            })
    
        return forward


# Emilia
def login(mail, password):
    '''
        Funktionen hämtar ut en lista med en specifik användare utifrån mail och lösenord från databasen.

        args:
            mail refererar till användaren som försöker logga in, mail.
        return:
            returnerar en lista med användarens mail och lösenord till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute ( """select mail, password
                                from fhl_user
                                    where mail=%s and password=%s""",
                                    (mail, password))
        user = cursor.fetchall()
    
    return user


# Emilia
def get_user(mail):
    '''
        Funktionen hämtar ut en användares mail från databasen.

        args:
            Syftar till användarens mail.
        return: 
            returnerar en lista med den aktuella användarens mail till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select mail
                            from fhl_user
                                where mail=%s""",
                                (mail,))
        user = cursor.fetchall()
    
    return user


# Marcus
def add_purchased_player_to_team(user_id, player_id):
    '''
    Funktion som lägger till köpt spelare till en användares lista över spelare
    '''
    with Postgres() as (cursor, conn): 

        cursor.execute("""select * from fhl_my_players""")
        user = cursor.fetchall()

        postgreSQL_insert = """ insert into fhl_my_players (fhl_user, player) values(%s, %s)"""
        insert_to = (user_id, player_id)

        cursor.execute(postgreSQL_insert, insert_to)

        conn.commit()


# Emilia
def registrations(username, mail, f_name, l_name, hash_password):
    '''
        Funktionen undersöker om användaren som försöker registrera sig redan finns i databasen. 
        Om användaren inte är registrerad så registreras denne.

        args:
            Argumenten som skickas med är variabler från fhl.py som användaren fyllt i när denna försöker registrera sig. 
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select mail, username from fhl_user
                                where  mail=%s""",
                                    (mail,))
        user = cursor.fetchall()

        if len(user)==0:
            points=100
            ranking = 0
            postgreSQL_insert = (""" insert into fhl_user (username, mail, f_name, l_name, password, points, ranking)
                                        values (%s, %s, %s, %s, %s, %s, %s) """)
                                            
            insert_to = (username, mail, f_name, l_name, hash_password, points, ranking)
            cursor.execute(postgreSQL_insert, insert_to)
            conn.commit()

        
    return user


# Emilia
def get_points(user_id):
    '''
        Funktionen hämtar ut en specifik användares aktuella poäng.

        args:
            syftar till den inloggade användaren.
        return:
            returnerar en lista med användarens poäng.
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select points
                            from fhl_user
                                where mail=%s""",
                                (user_id,))
        point = cursor.fetchall()
    
    return point


# Emilia
def delete_team_ranking():
    '''
        Funktionen raderar allt som finns i tabellen fhl_team_ranking i databasen om dagens datum inte stämmer 
        överrens med det datum som är inlagt i databasen. Funktionen körs från fhl.py.
    '''
    print ("delete team ranking")
    with Postgres() as (cursor, conn):
        postgreSQL_insert = (""" delete from fhl_team_ranking """)
        cursor.execute(postgreSQL_insert)
        conn.commit()


# Emilia
def insert_team_rank(all_teams):
    '''
        Funktionen lägger in nhl:S lags ranking i databasen. Funktionen körs efter att alla lag blivit raderade. Funktionen körs från fhl.py.

        args: 
            Lista med alla lags ranking med relevant information som hämtats från filen team_rank.py och nhl:s API.
    '''
    
    with Postgres() as (cursor, conn):
        for team in all_teams:
            postgreSQL_insert = (""" insert into fhl_team_ranking (team_name, team_loggo, games_played, wines, losses, ot, points, time_stamp)
                                        values (%s, %s, %s, %s, %s, %s, %s, %s) """)
                                            
            insert_to = (team["teamName"], team["teamLoggo"], team["gamesPlayed"], team["wines"], team["losses"], team["ot"], team["points"], team["timestamp"])
            
            cursor.execute(postgreSQL_insert, insert_to)
            conn.commit()


# Emilia
def get_timestamp_fhl_team_ranking (todays_date):
    '''
        Funktionen hämtar datumet från tabellen fhl_team_rank som finns i databasen.

        args:
            syftar till dagens datum som skickas med från fhl.py
        return:
            returnerar en lista med resultatet från sökningen i databasen till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select time_stamp
                            from fhl_team_ranking
                                where time_stamp=%s 
                                    limit 1""",
                                (todays_date,))
        list = cursor.fetchall()
    
    return list


# Emilia
def get_team_rank():
    '''
        Funktionen hämtar ut lagstatistiken från tabellen fhl_team_rank som finns i databasen och skickar denna till fhl.py.

        return:
            returnerar en lista med all information från tabellen fhl_team_ranking till fhl.py
    '''
    
    with Postgres() as (cursor, conn):
        cursor.execute("""select *
                            from fhl_team_ranking
                                order by points desc """)
        team_rank= cursor.fetchall()
        
    return team_rank


# Emilia
def delete_play_schedual():
    '''
        Funktionen redarer allt från tabellen fhl_tame_schedual i databasen om dagens datum inte är samma som datumet i tabellen. 
        Funktioen kallas från fhl.py
    '''

    with Postgres() as (cursor, conn):
        postgreSQL_insert = (""" delete from fhl_game_schedual """)
        cursor.execute(postgreSQL_insert)
        conn.commit()


# Emilia 
def insert_play_schedual(current_days_games):
    '''
        Funktionen lägger in schemat för dagens matcher i tabellen fhl_game_schedual i databasen efter att tidigare data blivit raderat.
        Funktionen kallas på från play_schedual.py.

        args:
            Lista med dagens matcher och tillhörande information som kommer från fhl_schedual och har hämtats från nhl:s api.
    '''
    with Postgres() as (cursor, conn):
        for play in current_days_games:
            postgreSQL_insert = (""" insert into fhl_game_schedual (team_away_name, team_away_loggo, game_date, game_time, team_home_name, team_home_loggo)
                                        values (%s, %s, %s, %s, %s, %s) """)
                                            
            insert_to = (play["team_away_name"], play["team_away_loggo"], play["game_date"], play["game_time"], play["team_home_name"], play["team_home_loggo"])
            
            cursor.execute(postgreSQL_insert, insert_to)
            conn.commit()


# Emilia
def get_date_fhl_game_schedual (todays_date):
    '''
        Funktionen hämtar ut en lista med dagens datum från tabellen fhl_game_schedual i databasen
        args:
            variabel med dagens datum
        return:
            returnerar en lista med dagens datum om denna finns i tabellen, till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select game_date
                            from fhl_game_schedual
                                where game_date=%s 
                                    limit 1""",
                                (todays_date,))
        list = cursor.fetchall()
    
    return list


# Emilia
def get_game_schedual():
    '''
        Funktionen hämtar dagens match schema från fhl_game_schedual från databasen. 

        return:
            returnerar en lista med dagens matcher till fhl.py
    '''
    
    with Postgres() as (cursor, conn):
        cursor.execute("""select *
                            from fhl_game_schedual
                                order by game_time """)
        schedual= cursor.fetchall()
        
    return schedual


# Emilia
def get_fhl_highscore():
    '''
        Funktionen hämtar ut de 5 spelarna som har högst ranking från fhl_user.

        return:
            returnerar en list användarnamn och ranking med de 5 bästa spelarna till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select username, ranking 
                            from fhl_user
                                where ranking is not null
                                order by ranking desc
                                    limit 5""")
        highscore= cursor.fetchall()
        
    return highscore


# Lukas
def post_forum(user_id):
    """
    Funktionen lägger till ett foruminlägg till databasen
    """
   
    with Postgres() as (cursor, conn):
        todaydate = date.today()
        now = datetime.now()
        todaytime = now.strftime("%H:%M:%S")
        fhl_user = user_id
        title = request.form.get("titlee")
        category = request.form.get("categoryy")
        text = request.form.get("textt")
        likes = 0 

        PostgreSQL_insert = """ INSERT INTO fhl_forum_form (date, datetime, fhl_user, title, category, text, likes) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_to = (todaydate, todaytime, fhl_user, title, category, text, likes)
        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()
        count = cursor.rowcount

        cursor.close()
        conn.close()


# Lukas
def post_forum_redirect():
    """
    Funktionen redirectar en användare efter att ha skapat ett inlägg
    """
    with Postgres() as (cursor, conn):
        cursor.execute("""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                            from fhl_forum_form
                            join fhl_user
                            on fhl_forum_form.fhl_user = fhl_user.mail""")
        data = cursor.fetchall()
        fhldata = data
        return fhldata


# Lukas
def get_all_forum():
    """
    Funktionen hämtar all forumdata vilket används för att visa alla inlägg
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                from fhl_forum_form
                join fhl_user
                on fhl_forum_form.fhl_user = fhl_user.mail 
                """)
            data = cursor.fetchall()
            fhldata=data
    return fhldata
    return fhldata


# Lukas
def get_category_forum(category):
    """
    Funktionen hämtar all forumdata inom en specifik kategori vilket används för att visa alla inlägg inom denna
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):

            if category == 'all':
                        cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                            from fhl_forum_form
                            join fhl_user
                            on fhl_forum_form.fhl_user = fhl_user.mail 
                            order by date desc """)

            else:
                cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                        from fhl_forum_form
                        join fhl_user
                        on fhl_forum_form.fhl_user = fhl_user.mail where category ='{category}'
                        order by date desc; """)
                
            data = cursor.fetchall()
            fhldata=data
    return fhldata
    return fhldata


# Lukas
def get_forum_username(user_id):
    """
    Funktionen hämtar alla forumdata som den inloggade användaren skapat vilket används för att visa alla inlägg
    """
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                        from fhl_forum_form
                        join fhl_user
                        on fhl_forum_form.fhl_user = fhl_user.mail
                        where fhl_user = '{user_id}'""")
        fhluserdata = cursor.fetchall()

    return fhluserdata


# Lukas
def delete_article_id(article_id):
    """
    Funktionen tar bort ett foruminlägg från databasen
    Args
        'article_id' from html submit
    """
    with Postgres() as (cursor, conn):
        delete_post = (f""" delete from fhl_forum_form where article_id = '{article_id}'""")
        cursor.execute(delete_post)
        conn.commit()


# Lukas
def like_article_id(article_id):
    """
    Funktionen gillar ett foruminlägg genom att uppdatera antalet gilla-markeringar i databasen
    Args
        'article_id' from html submit
    """
    with Postgres() as (cursor, conn):
        like_article_id = (f"""UPDATE fhl_forum_form set likes = (likes + 1) where article_id = '{article_id}'""")
        cursor.execute(like_article_id)
        conn.commit()


# Marcus
def add_chosen_players_to_game(left_forward, center, right_forward, left_defense, right_defense, goalie, user_id_form, team_name):
    '''
    Funktion som lägger till valda spelare när användaren lägger ett lag
    '''
    with Postgres() as (cursor, conn):

        todaydate = date.today()

        PostgreSQL_insert = """ INSERT INTO fhl_team (team_name, left_forward, right_forward,
        center, left_back, right_back, goalkeeper, fhl_user, team_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_to = (team_name, left_forward, center, right_forward, left_defense, right_defense, goalie, user_id_form, todaydate)

        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()

        cursor.close()
        conn.close()


# Emilia
def get_team_list_fhl_team():
    """
        Funktionen hämtar ut en lista med alla lag i databasen som inte har någon match_score än.
    """
    with Postgres() as (cursor, conn):
        cursor.execute("""select * from fhl_team 
                            where match_score is null""")
        team_list = cursor.fetchall()
    return team_list


# Marcus 
def get_todays_team_list(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar en lista med det skapade lag som ska användes vid match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select team_date from fhl_team 
                            where fhl_user='{user_id}' and team_date= '{todaydate}'""")
        team_list = cursor.fetchall()
    return team_list


# Marcus
def get_todays_left_forward(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar vänster forward som användes vid spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.left_forward 
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        left_forward = cursor.fetchall()
    return left_forward


# Marcus
def get_todays_right_forward(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar höger forward som användes vid spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.right_forward 
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        right_forward = cursor.fetchall()
    return right_forward


# Marcus
def get_todays_center(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar center användes i match som spelats 
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.center 
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        center = cursor.fetchall()
    return center


# Marcus
def get_todays_left_back(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar vänster back som användes vid spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.left_back 
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        left_back = cursor.fetchall()
    return left_back


# Marcus
def get_todays_right_back(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar höger back som användes vid spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.right_back
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        right_back = cursor.fetchall()
    return right_back


# Marcus
def get_todays_goalie(todaydate, user_id):
    '''
    Funktion som hämtar och returnerar målvakten som användes vid spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team 
                                join fhl_players on fhl_players.id = fhl_team.goalkeeper
                            where fhl_team.fhl_user='{user_id}' and fhl_team.team_date= '{todaydate}'""")
        goalie = cursor.fetchall()
    return goalie


# Marcus
def insert_team_score(team_score, team_id):
    """
        Funktionen lägger in match_score i databasen till specifika lag. 
        args:
            team_score- variabel med ett visst lag sammanlaggda poäng.
            team_id- variabel med ett visst lags id.
    """
    with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""update fhl_team
                                set match_score = {team_score}
                                    where team_id ={team_id}""")
        
        cursor.execute(PostgreSQL_insert)
        conn.commit()


# Marcus 
def get_other_users_lineup(user_id):
    '''
    Hämtar en annan användares lineup som användes vid en spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team where fhl_user != '{user_id}';""")
        teams= cursor.fetchall()
        
    return teams


# Marcus 
def get_users_lineup(user_id):
    '''
    Hämtar en användares lineup som användes vid en spelad match
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team where fhl_user = '{user_id}';""")
        teams= cursor.fetchall()
        
    return teams


# Marcus
def add_game_to_match_history(team_1, team_2, winner, looser):
    '''
    Funktion som lägger till en match i matchhistorik med lagens id, vinnare och förlorare
    '''
    with Postgres() as (cursor, conn):

        todaydate = date.today()

        PostgreSQL_insert = """ INSERT INTO fhl_match_history (team_1, team_2, winner, loser,
        match_date) VALUES (%s, %s, %s, %s, %s)"""
        insert_to = (team_1, team_2, winner, looser, todaydate)

        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()


# Marcus
def update_points(new_points, user_id):
     with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""update fhl_user
                                set points = {new_points}
                                    where mail ='{user_id}' """)
        
        cursor.execute(PostgreSQL_insert)
        conn.commit()

def update_points_after_win(user_id):
    '''
    Funktion ökar en spelares poäng med 50 i databasen efter man har vunnit en match.
    '''
    with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""update fhl_user
                                set points = points + 50
                                    where mail ='{user_id}' """)
        
        cursor.execute(PostgreSQL_insert)
        conn.commit()


# Lukas, Simon, Alexander
def update_points_after_bought_player(player_price, user_id):
    """
    Funktionen drar bort spelarens kostnad från den inloggade användarens poäng
    Args
        player_price = spelarens pris
        user_id = den inloggade användarens id
    """
    with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""UPDATE fhl_user SET points = (points - '{player_price}') WHERE mail ='{user_id}'""")

        cursor.execute(PostgreSQL_insert)
        conn.commit()


# Lukas, Simon, Alexander
def update_points_after_sell_player(player_id, player_price, user_id):
    """
    Funktionen säljer en spelare från den inloggade användarens lag samt adderar spelarens pris till användarens poäng
    Args
        player_id = spelarens id
        player_price = spelarens pris
        user_id = den inloggade användarens id
    """
    with Postgres() as (cursor, conn):
        sell_player = (f""" delete from fhl_my_players where player = '{player_id}' and fhl_user = '{user_id}'""")
        cursor.execute(sell_player)
        conn.commit()

    with Postgres() as (cursor, conn):
        update_player_points = (f"""UPDATE fhl_user SET points = (points + '{player_price}') WHERE mail ='{user_id}'""")
        cursor.execute(update_player_points)
        conn.commit()


# Marcus
def revert_points_after_error(player_price, user_id):
    with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""UPDATE fhl_user SET points = (points + '{player_price}') WHERE mail ='{user_id}'""")

        cursor.execute(PostgreSQL_insert)
        conn.commit()


# Marcus 
def update_ranking_after_win(user_id):
    '''
    Funktion ökar en spelares ranking med 5 i databasen efter man har vunnit en match.
    '''
    with Postgres() as (cursor, conn):
        PostgreSQL_insert = (f"""update fhl_user
                                set ranking = ranking + 5
                                    where mail ='{user_id}'""")
        
        cursor.execute(PostgreSQL_insert)
        conn.commit()


# Marcus
def get_history_won_games(user_id):
    '''
    Funktion som hämtar ut specifik matchhistorik för vunna matcher, där användarnamn och match score visas upp. Returnerar vinster
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select m.*, u.*, q.username, t.team_name as my_team, t.match_score as my_score, s.match_score as opponent_score, s.team_name as opponent from fhl_match_history m
                            join fhl_user as u
                                on m.winner=u.mail
                                    join fhl_team as t
                                        on m.team_1 = t.team_id 
                                            join fhl_team as s
                                                on m.team_2 = s.team_id
                                                    join fhl_user as q
                                                        on m.loser = q.mail
                                                            where m.winner='{user_id}';""")
        wins= cursor.fetchall()
        
        return wins


# Marcus
def get_history_lost_games(user_id):
    '''
    Funktion som hämtar ut specifik matchhistorik för förlorade matcher, där användarnamn och match score visas upp. Returnerar förluster
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select m.match_date, m.match_id, u.*, q.username, t.team_name as opponent_team, t.match_score as opponent_score, s.match_score as my_score, s.team_name as my_team from fhl_match_history m
                            join fhl_user as u
                                on m.loser=u.mail
                                    join fhl_team as t
                                        on m.team_1 = t.team_id 
                                            join fhl_team as s
                                                on m.team_2 = s.team_id
                                                    join fhl_user as q
                                                        on m.winner = q.mail
                                                        where m.loser='{user_id}';""")
        teams= cursor.fetchall()
        
    return teams


# Marcus 
def get_losses(user_id):
    '''
    Funktion som hämtar ut antal förluster från databasen och returnerar detta till matchhistoriken
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select loser, count(*) as amount 
                            FROM fhl_match_history
                                where loser = '{user_id}'
                                    group by loser;""")
        losses_sql = cursor.fetchall()
        losses = losses_sql[0]
        
        return losses


# Marcus 
def get_wins(user_id):
    '''
    Funktion hämtar ut antal vinster från databasen och returnerar detta till matchhistoriken
    '''
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select winner, count(*) as amount 
                            FROM fhl_match_history
                                where winner = '{user_id}'
                                    group by winner;""")
        wins_sql = cursor.fetchall()
        wins = wins_sql[0]  
        return wins