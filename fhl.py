#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect
from datetime import date
from datetime import datetime
import database
import  flask_login 
import hashlib
from database import *
import team_rank
import play_schedual



#Application 
FHL = Flask(__name__)


#Index 
@FHL.route('/')
@flask_login.login_required
def index():
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()

    points=get_user_points()

    return render_template('index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, points=points)


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
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    points=get_user_points()
    return render_template('index.html', points=points, teams_ranking=teams_ranking, game_schedual=game_schedual)


#Sign out
@FHL.route('/logout')
def logout():
    flask_login.logout_user()
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual)


#index för icke inloggade
@login_manager.unauthorized_handler
def unauthorized_handler():
    todaydate = date.today()
    rank_date_list=database.get_timestamp_fhl_team_ranking(todaydate)

    schedual_date_list=database.get_date_fhl_game_schedual (todaydate)

    if len(rank_date_list) < 1:
        database.delete_team_ranking()
        team_rank.get_team_rank()

    teams_ranking=database.get_team_rank()

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual)


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

    # Skapa if return beroende på output
    
    return render_template('index.html')


#Guide
@FHL.route('/guide/')
def guide():
    points=get_user_points()
    return render_template('guide.html', points=points)


#Buy players
@FHL.route('/köp-spelare/')
@flask_login.login_required
def buy_players():
    '''
    Funktion som först hämtar hur mycket poäng användaren har genon get_user_points() som finns i
    database.py och sedan hämtar alla spelare som finns genom get_all_players() som också finns i 
    database.py

    När användaren sedan klickar på köp i html filen buy_players skickas ett formulär tillbaka
    med id för den spelare som ska köpas. Sedan i funktionen add_purchased_player_to_team()
    skickas spelaren och användarens id med och läggs sedan till i databasen
    '''
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
    Den inloggade användarens mail sparas i denna: current_user.id. denna används för att ta ut saker ur databasen.
    Hämtar poäng och sedan vilka spelare som användaren har genom get_users_players() med användarens mail som 
    parameter.
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
    """
    Funktionen visar samtliga foruminlägg
    """
    points=get_user_points()
    fhldata=get_forum()
    return render_template('forum.html', points=points, fhldata=fhldata)

    
#Forum posts created by logged in user
@FHL.route('/forum/mina/inlägg/')
@flask_login.login_required
def forum_username():
    """
    Funktionen visas den inloggade användarens foruminlägg
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    fhluserdata = get_forum_username(user_id)
    return render_template('forum.html', points=points, fhluserdata=fhluserdata)


#Forum form for creating new post
@FHL.route('/inlägg/')
@flask_login.login_required
def write_post():
    """
    Functionen låter användaren skapa ett nytt foruminlägg
    """
    points=get_user_points()
    #user_id=flask_login.current_user.id? 
    return render_template('write_post.html', points=points)


#New post form data
@FHL.route('/form', methods=['POST'])
def form():
    """
    Funktionen sparar ett foruminlägg till databasen
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
    points=database.get_points(user_id)
    
    for i in points:
        points=i[0]
        
    
    print(points)
    return points




#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)