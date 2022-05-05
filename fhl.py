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

    print(teams_ranking)

    if len(schedual_date_list) < 1:
        database.delete_play_schedual()
        play_schedual.get_play_schedual ()
    
    game_schedual=database.get_game_schedual()
    highscore =database.get_fhl_highscore()
    points=get_user_points()

    return render_template('index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, points=points, highscore=highscore)


#Sign in
FHL.secret_key='hej' #ändra senare!
login_manager=flask_login.LoginManager()
login_manager.init_app (FHL)
@FHL.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Funktionen visar html filen login.html om användaren klickar på "logga in" på webbsidan.
    Funktionen hämtar datan som användaren fyllt in när denne försöker logga in. 
    Lösenordet krypteras.
    mail och lösenord skickas in i database.py för att kolla om datan finns i databasen eller inte. 
    Om listan med mail och lösenord är längre än o så loggas användaren in och redirectas till index.html.
    '''

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
    

class User (flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(mail):
    '''
        Funktionen sätter user.id till användarens mail. (En del av Flask_login)
        return:
            returnerar användarens mail som user.
    '''
    user = User()
    user.id = mail
    return user


#Index
@FHL.route('/protected')
@flask_login.login_required 
def protected():
    '''
        När användaren loggats in körs denna funktionen.

        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till index.html tillsammans med användarens poäng

        return:
             returnerar index.html tillsammans med lagranking, spelschema, och poäng och highscore.

    '''
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
    highscore =database.get_fhl_highscore()
    points=get_user_points()
    return render_template('index.html', points=points, teams_ranking=teams_ranking, game_schedual=game_schedual, highscore=highscore)


#Sign out
@FHL.route('/logout')
def logout():
    '''
        Funktionen loggar ut användaren.
        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till unauthorized_index.html

        return:
            returnerar unauthorized_index.html tillsammans med lagranking, spelschema och highscore.
    '''
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
    highscore =database.get_fhl_highscore()

    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, highscore=highscore)


#index för icke inloggade
@login_manager.unauthorized_handler
def unauthorized_handler():
    '''
        Funktionen hanterar om användaren inte är inloggad.
        Funktionen skickar in dagens datum till database.py för att få se om dagens datum finns i tabellen fhl_team_ranking i databasen.
        Om listan är mindre än 1 så körs fuktionen delete_team_ranking i database.py och funktionen get_team_rank i team_rank.py.

        Funktionen skickar in dagens daturm till database. py för att se om dagens datum finns i tabellen fhl_game_schedual.
        Om listan är mindre än 1 så körs funktionen delete_play_schedual i database.py och funktioen get_play_schedual från play_schedual.py

        Funktionen hämtar get_game_schedual, get_team_rank, get_fhl_highscore från database.py och skickar med dessa listor till unauthorized_index.html

        return:
            returnerar unauthorized_index.html tillsammans med lagranking, spelschema och highscore.
    '''
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
    highscore =database.get_fhl_highscore()
    return render_template('unauthorized_index.html', teams_ranking=teams_ranking, game_schedual=game_schedual, highscore=highscore)


#Registration
@FHL.route('/registration', methods=['GET','POST'])
def registration():
    '''
        Funktionen ger användaren registration.html när denne klickar på "Registrera".
        Funktionen tar emot värdena som användaren fyllt i i formuläret på registration.html och skickar dessa till databasen för att som om dessa finns lagrade eller inte.
        Om mailen redan finns registrerad så returneras registration.html tillbaka med felmeddelande om att mailen redan finns registreras. 
        Om användarnamnet redan finns registrerat så returneras registration.html tillbaka med felmeddelande om att användarnamnet redan finns. 
        Annars kommer kommer användarnen in i systemet.

    '''
    if request.method == 'GET':
        return render_template('registration.html')
    
    f_name=request.form['fname']
    l_name=request.form['lname']
    mail=request.form['mail']
    username=request.form['username']
    password=request.form['password']
    hash_password=hashlib.md5(password.encode()).hexdigest()

    user=database.registrations(username, mail, f_name, l_name, hash_password)

    for person in user:
        if person[0]==mail:
            return render_template("registration.html", existing_mail="Mailadressen du försöker använda finns redan registrerat, vänligen ange en annan mailadress eller logga in.")
        elif person[1]==username:
            return render_template("registration.html", existing_username="Användarnamnet du försöker använda finns redan registrerat, vänligen välj ett annat användarnamn ")
        
    return render_template('index.html')


#Guide
@FHL.route('/guide/')
def guide():
    points=get_user_points()
    return render_template('guide.html', points=points)


#Buy players
@FHL.route('/köp-spelare/', methods = ['GET', 'POST'])
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

    right_forwards = get_right_forward_players()
    centers = get_center_players()
    left_forwards = get_left_forward_players()
    defense = get_defense_players()
    goalies = get_goalie_players()

    if request.method == 'POST':
        player_id = request.form['id']
        user_id=flask_login.current_user.id

        add_purchased_player_to_team(user_id, player_id)
    
    return render_template('buy_players.html', points=points, right_forwards = right_forwards, centers = centers,
    left_forwards = left_forwards, defense = defense, goalies = goalies)

@FHL.route('/spela-match/', methods= ['GET', 'POST'])
@flask_login.login_required
def play_game():
    '''
    Route för att spela match
    '''

    user_id=flask_login.current_user.id
    teams = get_other_users_lineup(user_id)
    my_teams = get_users_lineup(user_id)

    if request.method == 'POST':

        opponent_team_form = request.form['opponent_team'].split(", ")
        opponent_score = int(opponent_team_form[0])
        opponent_user = opponent_team_form[1]

        my_team_score_str = request.form['my_team']
        my_team_score = int(my_team_score_str)
        my_team_user = user_id

        if my_team_score > opponent_score:
            print("Du vinner!")
            winner = my_team_user
            looser = opponent_user

            #add_game_to_match_history(my_team_user, opponent_user, winner, looser)
            #Användaren får poäng

        elif my_team_score < opponent_score:
            print("Du förlorar!")
            winner = opponent_user
            looser = my_team_user

            #add_game_to_match_history(my_team_user, opponent_user, winner, looser)
            #Andra spelaren får poäng

        else:
            print("Vad ska vi göra när det blir lika?")


    return render_template('play_game.html', teams = teams, my_teams = my_teams)

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
    goalie = get_users_goalie(user_id)
    defenseman = get_users_defenseman(user_id)
    forward = get_users_forward(user_id)
    center = get_users_center(user_id)
    return render_template('my_players.html', points=points, goalie=goalie, defenseman=defenseman, center=center, forward=forward)


#Game
@FHL.route('/match/', methods = ['GET', 'POST'])
@flask_login.login_required
def match():
    points=get_user_points()
    user_id=flask_login.current_user.id
    goalie = get_users_goalie(user_id)
    defenseman = get_users_defenseman(user_id)
    left_wing = get_users_left_wing(user_id)
    center = get_users_center(user_id)
    right_wing = get_users_right_wing(user_id)

    if request.method == 'POST':
        left_forward_form = request.form['left_forward'].split(", ")
        left_forward_id = left_forward_form[0]
        left_forward_score = left_forward_form[1]

        center_form = request.form['center'].split(", ")
        center_id = center_form[0]
        center_score = center_form[1]

        right_forward_form = request.form['right_forward'].split(", ")
        right_forward_id = right_forward_form[0]
        right_forward_score = right_forward_form[1]

        left_defense_form = request.form['left_defense'].split(", ")
        left_defense_id = left_defense_form[0]
        left_defense_score = left_defense_form[1]

        right_defense_form = request.form['right_defense'].split(", ")
        right_defense_id = right_defense_form[0]
        right_defense_score = right_defense_form[1]

        goalie_form = request.form['goalie'].split(", ")
        goalie_id = goalie_form[0]
        goalie_score = goalie_form[1]

        team_name = request.form['team_name']

        score = int(left_forward_score) + int(center_score) + int(right_forward_score) + int(left_defense_score) + int(right_defense_score) + int(goalie_score)

        user_id=flask_login.current_user.id

        add_chosen_players_to_game(left_forward_id, center_id, right_forward_id, left_defense_id, 
        right_defense_id, goalie_id, user_id, score, team_name)


    return render_template('match.html', points=points, goalie=goalie, defenseman=defenseman, left_wing=left_wing, center=center, right_wing=right_wing)


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