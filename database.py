import psycopg2
import sys 
from datetime import date
from datetime import datetime
from connect import Postgres


def get_all_players():
    with Postgres() as (cursor, conn):
        cursor.execute ("""select * from fhl_players""")
        players=cursor.fetchall()

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
 