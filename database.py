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
        info = cursor.fetchall()

        players = []

        for list in info:
            f_name = list[1]
            players.append({
                "f_name": f_name
            })
            


        print(players)

        cursor.close()
        return players



    except (Exception, Error) as error:
        print("Error while connectin to PostgreSQL", error)


    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()

get_all_players()