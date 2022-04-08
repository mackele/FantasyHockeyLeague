#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error
from datetime import date
from datetime import datetime


#Application 
FHL = Flask(__name__)


#SQL connect (Create function)
def fhl_database_connect():
    """
    Function allows user to connect to database
    """ 


#SQL disconnect (Create function)
def fhl_database_disconnect():
    """
    Function allows user to disconnect from database
    """

#SQL-SELECT connect to route (Change)
connection = psycopg2.connect(user="grupp2_onlinestore", 
password="n8siil4c",
host="pgserver.mau.se",
port="5432",
database="grupp2_onlinestore")
cursor = connection.cursor()


#Index 
@FHL.route('/')
def index():
    return render_template('index.html')


#Sign in
@FHL.route('/login/')
def login():
    return render_template('login.html')


#Sign up
@FHL.route('/registrera/')
def registration():
    return render_template('registration.html')


#Guide
@FHL.route('/guide/')
def guide():
    return render_template('guide.html')


#Buy players
@FHL.route('/köp-spelare/')
def buy_players():
    return render_template('buy_players.html')


#My players
@FHL.route('/mina-spelare/')
def my_players():
    return render_template('my_players.html')


#Game
@FHL.route('/match/')
def match():
    return render_template('match.html')


#Game history
@FHL.route('/match-historik/')
def match_history():
    return render_template('matchhistory.html')


#Toplist
@FHL.route('/top-spelare')
def top_scorer():
    return render_template('topscorer.html')


#Forum
@FHL.route('/forum/')
def forum():
    cursor.execute("""select * from fhl_forum_form""")
    data = cursor.fetchall()
    return render_template('forum.html', fhldata=data)


#Forum posts
@FHL.route('/inlägg/')
def write_post():
    return render_template('write_post.html')


#New post form data
@FHL.route('/form', methods=['POST'])
def form():
    """
    Function inserts post to database
    """

    #Connect to FHL Database
    try: 
        connection = psycopg2.connect(user="grupp2_onlinestore", 
        password="n8siil4c",
        host="pgserver.mau.se",
        port="5432",
        database="grupp2_onlinestore")
        cursor = connection.cursor()
        

        #Need to add .get in order to function as variable and INSERT to database
        todaydate = date.today()
        now = datetime.now()
        todaytime = now.strftime("%H:%M:%S")
        #Username (Change)
        username = "NA"
        title = request.form.get("title")
        category = request.form.get("category")
        text = request.form.get("text")
        #Static for now, a Could for later! (Change)
        likes = 21 


        PostgreSQL_insert = """ INSERT INTO fhl_forum_form (date, datetime, username, title, category, text, likes) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        insert_to = (todaydate, todaytime, username, title, category, text, likes)
        cursor.execute(PostgreSQL_insert, insert_to)

        connection.commit()
        count = cursor.rowcount


    except (Exception, Error) as error:
        print("Error while connectin to FHL Database", error)
        

    #Close connection to FHL Database
    finally:
        if connection:
            cursor.close()
            connection.close()
            
            #Redirect
            connection = psycopg2.connect(user="grupp2_onlinestore", 
            password="n8siil4c",
            host="pgserver.mau.se",
            port="5432",
            database="grupp2_onlinestore")
            cursor = connection.cursor()
            cursor.execute("""select * from fhl_forum_form""")
            data = cursor.fetchall()
            return render_template('forum.html', fhldata=data)


#Form posts categorized (Not working)
@FHL.route('/category', methods=['POST','GET'])
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
get_form()




#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)