import psycopg2
import sys 
from datetime import date
from datetime import datetime
from connect import Postgres


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
            id = list[0],
            f_name = list[1],
            l_name = list[2],
            team = list[3],
            position = list[4],
            goal = list[5],
            penalty_time = list[6],
            assists = list[7],
            description = list[8],
            image = list[9],
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
       

        
def registrations(username, mail, f_name, l_name, password):
    with Postgres() as (cursor, conn):
        cursor.execute("""select user_name, mail from fhl_user
                                where user_name=%s or mail=%s""",
                                    (username, mail))
        user = cursor.fetchall()

        if len(user)==0:
            points=100
            postgreSQL_insert = (""" insert into fhl_user (user_name, mail, f_name, l_name, password, points)
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