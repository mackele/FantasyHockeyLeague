import psycopg2
import sys 
from datetime import date
from datetime import datetime
from connect import Postgres
from flask import Flask, render_template, redirect, url_for, request, redirect
from psycopg2.extras import execute_values


def add_goalie_to_database(goalies):
    '''
    Funktion som lägger in målvakter som hämtas i en lista med lexikon från APIn i test.py
    '''

    with Postgres() as (cursor, conn):
        cursor.execute("""select * from fhl_players""")
        

        columns = goalies[0].keys()
        query = "INSERT INTO fhl_players ({}) VALUES %s".format(','.join(columns))
        values = [[value for value in goalie.values()] for goalie in goalies]

        execute_values(cursor, query, values)
        conn.commit()
        

def add_player_to_database(players):
    '''
    Funktion som lägger in spelare som hämtas i en lista med lexikon från APIn i test.py
    '''

    with Postgres() as (cursor, conn):
        cursor.execute("""select * from fhl_players""")
        
        columns = players[0].keys()
        query = "INSERT INTO fhl_players ({}) VALUES %s".format(','.join(columns))
        values = [[value for value in player.values()] for player in players]

        execute_values(cursor, query, values)
        conn.commit()


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


def get_center_players():
    """
    Funktion som hämtar alla center spelare till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: center_players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players where position = 'Center' order by price desc""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


def get_right_forward_players():
    """
    Funktion som hämtar alla höger forward spelare till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: center_players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players where position = 'Right Wing' order by price desc""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


def get_left_forward_players():
    """
    Funktion som hämtar alla vänster forward spelare till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: center_players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players where position = 'Left Wing' order by price desc""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


def get_defense_players():
    """
    Funktion som hämtar alla backar till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: center_players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players where position = 'Defenseman' order by price desc""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


def get_goalie_players():
    """
    Funktion som hämtar alla målvakter till en lista av lexikon som sedan används i fhl.py för att printa ut 
    spelarkort.

        Returns: center_players
        Detta är en lista av lexikon med samtliga värden
    """
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players where position = 'Goalie' order by price desc""")
        info=cursor.fetchall()

        players = add_players_to_list(info)

        return players


def get_users_players(user_id):
    '''
        Funktion som hämtar den inloggade användarens köpta hockeyspelare.

        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_goalie(user_id):
    '''
        Funktion hämtar användarens goalies
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_defenseman(user_id):
    '''
        Funktion hämtar användarens defenseman
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_left_wing(user_id):
    '''
        Funktion hämtar användarens left wings
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_center(user_id):
    '''
        Funktion hämtar användarens centers
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_right_wing(user_id):
    '''
        Funktion hämtar användarens right wings
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def get_users_forward(user_id):
    '''
        Funktion hämtar användarens forwards
        args:
            user_id är den inloggade användarens personliga id.
        return:
            Returnerar användarens köpta spelare till fhl.py
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


def add_purchased_player_to_team(user_id, player_id):
    with Postgres() as (cursor, conn): 

        cursor.execute("""select * from fhl_my_players""")
        user = cursor.fetchall()

        postgreSQL_insert = """ insert into fhl_my_players (fhl_user, player) values(%s, %s)"""
        insert_to = (user_id, player_id)

        cursor.execute(postgreSQL_insert, insert_to)

        conn.commit()


def registrations(username, mail, f_name, l_name, password):
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
            postgreSQL_insert = (""" insert into fhl_user (username, mail, f_name, l_name, password, points)
                                        values (%s, %s, %s, %s, %s, %s) """)
                                            
            insert_to = (username, mail, f_name, l_name, password, points)
            cursor.execute(postgreSQL_insert, insert_to)
            conn.commit()

        else:
            return user


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


def delete_team_ranking():
    '''
        Funktionen raderar allt som finns i tabellen fhl_team_ranking i databasen om dagens datum inte stämmer 
        överrens med det datum som är inlagt i databasen. Funktionen körs från fhl.py.
    '''
    with Postgres() as (cursor, conn):
        postgreSQL_insert = (""" delete from fhl_team_ranking """)
        cursor.execute(postgreSQL_insert)
        conn.commit()


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


def delete_play_schedual():
    '''
        Funktionen redarer allt från tabellen fhl_tame_schedual i databasen om dagens datum inte är samma som datumet i tabellen. 
        Funktioen kallas från fhl.py
    '''

    with Postgres() as (cursor, conn):
        postgreSQL_insert = (""" delete from fhl_game_schedual """)
        cursor.execute(postgreSQL_insert)
        conn.commit()


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


def get_fhl_highscore():
    '''
        Funktionen hämtar ut de 5 spelarna som har högst ranking från fhl_user.

        return:
            returnerar en list användarnamn och ranking med de 5 bästa spelarna till fhl.py
    '''
    with Postgres() as (cursor, conn):
        cursor.execute("""select username, ranking 
                            from fhl_user
                                order by ranking desc
                                    limit 5""")
        highscore= cursor.fetchall()
        
    return highscore


def post_forum(user_id):
    """
    Function inserts post to database
    """
   
    with Postgres() as (cursor, conn):
        todaydate = date.today()
        now = datetime.now()
        todaytime = now.strftime("%H:%M:%S")
        fhl_user = user_id
        title = request.form.get("titlee")
        category = request.form.get("categoryy")
        text = request.form.get("textt")
        likes = 21 

        PostgreSQL_insert = """ INSERT INTO fhl_forum_form (date, datetime, fhl_user, title, category, text, likes) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_to = (todaydate, todaytime, fhl_user, title, category, text, likes)
        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()
        count = cursor.rowcount

        cursor.close()
        conn.close()


def post_forum_redirect():
    """
    Function redirects user after saving post
    """
    with Postgres() as (cursor, conn):
        cursor.execute("""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                            from fhl_forum_form
                            join fhl_user
                            on fhl_forum_form.fhl_user = fhl_user.mail""")
        data = cursor.fetchall()
        fhldata = data
        return fhldata


#Default for forum 
def get_all_forum():
    """
    Function retrieves all form data
    Used to display forum posts
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                from fhl_forum_form
                join fhl_user
                on fhl_forum_form.fhl_user = fhl_user.mail """)
            data = cursor.fetchall()
            fhldata=data
    return fhldata
    return fhldata


def get_category_forum(category):
    """
    Function retrieves all form data
    Used to display forum posts
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):

            if category == 'all':
                        cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                            from fhl_forum_form
                            join fhl_user
                            on fhl_forum_form.fhl_user = fhl_user.mail """)

            else:
                cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                        from fhl_forum_form
                        join fhl_user
                        on fhl_forum_form.fhl_user = fhl_user.mail where category ='{category}'; """)
                
            data = cursor.fetchall()
            fhldata=data
    return fhldata
    return fhldata


def get_forum_username(user_id):
    """
    Function retrieves all form data posted by the logged in user
    Used to display forum posts
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            cursor.execute(f"""select date, datetime, article_id, fhl_user, title, category, text, likes, username 
                            from fhl_forum_form
                            join fhl_user
                            on fhl_forum_form.fhl_user = fhl_user.mail
                            where fhl_user = '{user_id}'""")
            fhluserdata = cursor.fetchall()

    return fhluserdata
    return fhluserdata


def delete_article_id(article_id):
    """
    Function deletes form post
    Args
        'article_id' from html submit
    """
    with Postgres() as (cursor, conn):
        delete_post = (f""" delete from fhl_forum_form where article_id = '{article_id}'""")
        cursor.execute(delete_post)
        conn.commit()


def add_chosen_players_to_game(left_forward, center, right_forward, left_defense, right_defense, goalie, user_id_form, score, team_name):
    with Postgres() as (cursor, conn):

        todaydate = date.today()

        PostgreSQL_insert = """ INSERT INTO fhl_team (team_name, match_score, left_forward, right_forward,
        center, left_back, right_back, goalkeeper, fhl_user, team_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        insert_to = (team_name, score, left_forward, center, right_forward, left_defense, right_defense, goalie, user_id_form, todaydate)

        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()

        cursor.close()
        conn.close()


def get_other_users_lineup(user_id):
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team where fhl_user != '{user_id}';""")
        teams= cursor.fetchall()
        
    return teams


def get_users_lineup(user_id):
    with Postgres() as (cursor, conn):
        cursor.execute(f"""select * from fhl_team where fhl_user = '{user_id}';""")
        teams= cursor.fetchall()
        
    return teams


def add_game_to_match_history(team_1, team_2, winner, looser):
    with Postgres() as (cursor, conn):

        todaydate = date.today()

        PostgreSQL_insert = """ INSERT INTO fhl_match_history (team_1, team_2, winner, loser,
        match_date) VALUES (%s, %s, %s, %s, %s)"""
        insert_to = (team_1, team_2, winner, looser, todaydate)

        cursor.execute(PostgreSQL_insert, insert_to)

        conn.commit()

        cursor.close()
        conn.close()