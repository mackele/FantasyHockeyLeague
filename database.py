import psycopg2
from psycopg2 import Error
import sys 
from datetime import date
from datetime import datetime


def get_all_players():
    """
    Function displays all products in store
    """

    
    #Connect to database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()
    
        cursor.execute("""select * from fhl_players""")
        players = cursor.fetchall()

        cursor.close()
        return players

        #print(players)

        for player in players:
            print(player)

        #for row in players:
         #   print("{:<25}{:<25}{:<25}{:<25}{:<25}{:<25}".format(row[0], row[1], row[2], row[3], f"{row[4]} kr/st", f"{row[5]} st"))
        
        cursor.close()


    except (Exception, Error) as error:
        print("Error while connectin to PostgreSQL", error)


    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()

def login(mail, password):
    """
    Function get users
    """
    #Connect to database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()
    
        cursor.execute("""select mail, password
                            from fhl_user
                                where mail=%s and password=%s""",
                                (mail, password))
        user = cursor.fetchall()

        cursor.close()
        

    except (Exception, Error) as error:
        print("Error while connectin to PostgreSQL", error)


    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()

    return user

def get_user(mail):
    """
    Function get users
    """
    #Connect to database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()
    
        cursor.execute("""select mail
                            from fhl_user
                                where mail=%s""",
                                (mail,))
        user = cursor.fetchall()

        cursor.close()
        

    except (Exception, Error) as error:
        print("Error while connectin to PostgreSQL", error)


    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()

    return user


def registrations(username, mail, f_name, l_name, password):
    """
    Function get users
    """
    #Connect to database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()

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
        connection.commit()
        cursor.close()
        

    except (Exception, Error) as error:
        print( error)
    
    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()

    return user