#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error

#Application 
FHL = Flask(__name__)


#SQL function connect 
#SQL function disconnect 


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
    return render_template('forum.html')


#Forum posts
@FHL.route('/inlägg/')
def write_post():
    return render_template('write_post.html')


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

        #In fhl_forum add variable fhl_user (foreign key to fhl_user(user_name))

        #Need to add .get in order to function as variable and INSERT to database
        title = request.form.get("title")
        category = request.form.get("category")
        text = request.form.get("text")
        likes = 21 

        PostgreSQL_insert = """ INSERT INTO forum_test (title, category, text, likes) VALUES (%s, %s, %s, %s)"""
        insert_to = (title, category, text, likes)
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
            return render_template('forum.html')




#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)