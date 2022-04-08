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
            

        cursor.close()
        return players



    except (Exception, Error) as error:
        print("Error while connectin to PostgreSQL", error)


    #Close database connection 
    finally:
        if connection:
            cursor.close()
            connection.close()
