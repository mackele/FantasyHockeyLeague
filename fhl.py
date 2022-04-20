#Imported modules 
from audioop import reverse
from operator import truediv
from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error
from datetime import date
from datetime import datetime
import database
import  flask_login 
import hashlib
from database import *


#Application 
FHL = Flask(__name__)


#Index 
@FHL.route('/')
@flask_login.login_required
def index():
    return render_template('unauthorized_index.html')


#Sign in
FHL.secret_key='hej' #ändra senare!
login_manager=flask_login.LoginManager()
login_manager.init_app (FHL)
@FHL.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    mail=request.form['mail']
    password=request.form['password']
    hash_password=hashlib.md5(password.encode()).hexdigest()
    user=database.login(mail, hash_password) 

    if len(user)>0:
        user=User()
        user.id=mail
        flask_login.login_user(user)
        return redirect(url_for('protected'))
    return 'Bad login'

class User (flask_login.UserMixin):
    pass
@login_manager.user_loader
def user_loader(mail):
    user = User()
    user.id = mail
    return user


#Index
@FHL.route('/protected')
@flask_login.login_required 
def protected():
    points=get_user_points()
    return render_template('index.html', points=points)


#Sign out
@FHL.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('unauthorized_index.html')


#index för icke inloggade
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized_index.html')


#Registration
@FHL.route('/registration', methods=['GET','POST'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    
    f_name=request.form['fname']
    l_name=request.form['lname']
    mail=request.form['mail']
    username=request.form['username']
    password=request.form['password']
    hash_password=hashlib.md5(password.encode()).hexdigest()

    user=database.registrations(username, mail, f_name, l_name, hash_password)
    print("fhl", user)
    
    return render_template('index.html')


#Guide
@FHL.route('/guide/')
def guide():
    points=get_user_points()
    return render_template('guide.html', points=points)


#Buy players
@FHL.route('/köp-spelare/', methods=['GET', 'POST'])
@flask_login.login_required
def buy_players():
    points=get_user_points()

    players = get_all_players()

    if request.method == 'POST':
        player_id = request.form['id']
        user_id=flask_login.current_user.id

        add_purchased_player_to_team(user_id, player_id)
    
    return render_template('buy_players.html', points=points, players = players)


#My players
@FHL.route('/mina-spelare/')
@flask_login.login_required
def my_players():

    """
    den inloggade användarens mail sparas i denna: current_user.id. denna används för att ta ut saker ur databasen.
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    players = get_users_players(user_id)
    
    return render_template('my_players.html', points=points, players = players)


#Game
@FHL.route('/match/')
@flask_login.login_required
def match():
    points=get_user_points()
    return render_template('match.html', points=points)


#Game history
@FHL.route('/match-historik/')
@flask_login.login_required
def match_history():
    points=get_user_points()
    return render_template('matchhistory.html', points=points)


#Toplist
@FHL.route('/top-spelare')
def top_scorer():
    points=get_user_points()
    '''
    Funktion skickar med sig en lista av lexikon players som hämtad från funktionen get_all_players som finns i 
    database.py. Denna lista sorteras sedan utifrån vad spelarkorten ska sorteras på, exempelvis mål, assist mm.
    '''

    players = get_all_players()
    top_players = sorted(players, key = lambda k: k['price'], reverse=True)
    most_goals = sorted(players, key = lambda k: k['goal'], reverse=True)
    most_assists = sorted(players, key = lambda k: k['assists'], reverse=True)
    return render_template('topscorer.html', players = players, top_players = top_players, most_goals = most_goals, most_assists = most_assists, points=points)


#Forum
@FHL.route('/forum/')
@flask_login.login_required
def forum():
    points=get_user_points()
    fhldata=get_forum()
    return render_template('forum.html', points=points, fhldata=fhldata)


#Forum posts created by logged in user
@FHL.route('/forum/mina/inlägg/')
@flask_login.login_required
def forum_username():
    points=get_user_points()
    user_id=flask_login.current_user.id
    fhluserdata = get_forum_username(user_id)
    return render_template('forum.html', points=points, fhluserdata=fhluserdata)


#Forum form for creating new post
@FHL.route('/inlägg/')
@flask_login.login_required
def write_post():
    points=get_user_points()
    #user_id=flask_login.current_user.id? 
    return render_template('write_post.html', points=points)


#New post form data
@FHL.route('/form', methods=['POST'])
def form():
    """
    Function inserts post to database
    """
    points=get_user_points()
    #current user_id sends to function post_forum
    user_id=flask_login.current_user.id
    post = post_forum(user_id)
    fhldata = post_forum_redirect()
    return render_template('forum.html', points=points, post=post, fhldata=fhldata)


#Logged in users points
@FHL.route('/points')
@flask_login.login_required
def get_user_points():
    user_id=flask_login.current_user.id
    
    print("hejpådig", user_id)
    points=database.get_points(user_id)
    
    for i in points:
        points=i[0]
        
    
    print(points)
    return points




#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)