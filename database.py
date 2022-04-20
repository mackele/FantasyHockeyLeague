import psycopg2
import sys 
from datetime import date
from datetime import datetime
from connect import Postgres
from flask import Flask, render_template, redirect, url_for, request, redirect


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

        players = []

        for list in info:
            id = list[0]
            f_name = list[1]
            l_name = list[2]
            team = list[3]
            position = list[4]
            goal = list[5]
            penalty_time = list[6]
            assists = list[7]
            description = list[8]
            image = list[9]
            price = list[10]

            players.append({
                "id": id,
                "f_name": f_name,
                "l_name": l_name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "description": description,
                "image": image,
                "price": price
            })

        return players

def get_users_players(user_id):

    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players 
            as f join fhl_my_players as m on f.id = m.player 
                where m.fhl_user = %s""", (user_id,))
        info=cursor.fetchall()

        players = []

        for list in info:
            id = list[0]
            f_name = list[1]
            l_name = list[2]
            team = list[3]
            position = list[4]
            goal = list[5]
            penalty_time = list[6]
            assists = list[7]
            description = list[8]
            image = list[9]
            price = list[10]

            players.append({
                "id": id,
                "f_name": f_name,
                "l_name": l_name,
                "team": team,
                "position": position,
                "goal": goal,
                "penalty_time": penalty_time,
                "assists": assists,
                "description": description,
                "image": image,
                "price": price
            })

        return players

def login(mail, password):
    with Postgres() as (cursor, conn):
        cursor.execute ( """select mail, password
                                from fhl_user
                                    where mail=%s and password=%s""",
                                    (mail, password))
        user = cursor.fetchall()
    
    return user

def get_user(mail):
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
    with Postgres() as (cursor, conn):
        cursor.execute("""select mail from fhl_user
                                where  mail=%s""",
                                    (mail,))
        user = cursor.fetchall()

        if len(user)==0:
            points=100
            postgreSQL_insert = (""" insert into fhl_user (username, mail, f_name, l_name, password, points)
                                        values (%s, %s, %s, %s, %s, %s) """)
                                            
            insert_to = (username, mail, f_name, l_name, password, points)
            print (username, mail, f_name, l_name, password, points)
            cursor.execute(postgreSQL_insert, insert_to)
            conn.commit()

def get_points(user_id):
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            cursor.execute("""select points
                                from fhl_user
                                    where mail=%s""",
                                    (user_id,))
            point = cursor.fetchall()
    
    return point
        
    return point

def post_forum():
    """
    Function inserts post to database
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            #Need to add .get in order to function as variable and INSERT to database
            todaydate = date.today()
            now = datetime.now()
            todaytime = now.strftime("%H:%M:%S")
            #Username (Change to username = logged in)
            fhl_user = "NA@gmail.com"
            title = request.form.get("title")
            category = request.form.get("category")
            text = request.form.get("text")
            #Static for now, a Could for later! (Change)
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
        cursor.execute("""select * from fhl_forum_form""")
        data = cursor.fetchall()
        fhldata = data
        return fhldata

def get_forum():
    """
    Function retrieves all form data
    Used to display forum posts
    """
    with Postgres() as (cursor, conn):
        with Postgres() as (cursor, conn):
            cursor.execute("""select * from fhl_forum_form""")
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
            #(Update to search for post where username = logged in username) 
            # (user_id=flask_login.current_user.id)???
            cursor.execute(f"""select * from fhl_forum_form where fhl_user='{user_id}'""")
            data = cursor.fetchall()
            fhluserdata = data
    return fhluserdata
    return fhluserdata

#Form posts categorized (Not working)
#@FHL.route('/category', methods=['POST','GET'])
def get_form():
    """
    Function displays posts in selected category 
    """

    #Connect to FHL Database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()
        
        #User select  
        category = 'player'
        #request.get.category('category')
        #cursor.execute (f""" SELECT * from fhl_forum_form where category = '{category}'; """)
        #data = cursor.fetchall()
        #return render_template('forum.html', fhldata=data)
        

        cursor.execute (f""" SELECT * from fhl_forum_form where category = '{category}'; """)
        fhldata = cursor.fetchall()

        for data in fhldata:
            print("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}".format(data[0], data[1], data[3], data[4],  data[5], data[6]))
        print("-"*150)
        cursor.close()


    except (Exception, Error) as error:
        print("Error while connectin to FHL Database", error)
        

    #Close connection to FHL Database
    finally:
        if connection:
            cursor.close()
            connection.close()
#get_form()