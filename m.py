import psycopg2
from psycopg2 import Error
import sys 
from datetime import date
from datetime import datetime

def print_players():
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

        print(players)

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

print_players()