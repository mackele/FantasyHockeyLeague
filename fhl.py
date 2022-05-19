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
import team_score



#Application 
FHL = Flask(__name__)


#Index 
@FHL.route('/')
@flask_login.login_required
def index():
    todaydate = date.today()
    print(todaydate)
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
    print(user)
    
    if len(user)>0:
        existing="Mailadressen eller användarnamnet du försökte använda finns redan, vänligen försök igen."
        return render_template('registration.html', existing=existing)
            
    else:
        
        return redirect(url_for('protected'))   


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
    När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
    Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.

    Funktion som först hämtar hur mycket poäng användaren har genon get_user_points() som finns i
    database.py och sedan hämtar alla spelare som finns genom get_all_players() som också finns i 
    database.py

    När användaren sedan klickar på köp i html filen buy_players skickas ett formulär tillbaka
    med id för den spelare som ska köpas. Sedan i funktionen add_purchased_player_to_team()
    skickas spelaren och användarens id med och läggs sedan till i databasen.
    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        print("Funktionen kommer att ta lång tid att köra, vänta ca 3 min.")
        team_score.insert_score_to_database()

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

#Play game
@FHL.route('/spela-match/', methods= ['GET', 'POST'])
@flask_login.login_required
def play_game():
    '''
    Route för att spela match
    '''
    points=get_user_points()
    user_id=flask_login.current_user.id
    teams = get_other_users_lineup(user_id)
    my_teams = get_users_lineup(user_id)

    if request.method == 'POST':

        opponent_team_form = request.form['opponent_team'].split(", ")
        opponent_score = int(opponent_team_form[0])
        opponent_user = opponent_team_form[1]
        opponent_team_id = int(opponent_team_form[2])

        my_team_form= request.form['my_team'].split(", ")
        my_team_score = int(my_team_form[0])
        my_team_user = user_id
        my_team_id = int(my_team_form[1])

        if my_team_score > opponent_score:
            print("Du vinner!")
            winner = my_team_user
            looser = opponent_user

            print("Mitt lag")
            print(my_team_score)
            print(my_team_user)
            print(my_team_id)

            print("Motståndare")
            print(opponent_score)
            print(opponent_user)
            print(opponent_team_id)

            add_game_to_match_history(my_team_id, opponent_team_id, winner, looser)
            
            #points = get_user_points
            
            update_points_after_win(user_id)
            update_ranking_after_win(user_id)

            new_points = get_user_points()

            return render_template('vinnare.html', new_points = new_points, my_score = my_team_score, opponent_score = opponent_score)

            #Användaren får poäng

        elif my_team_score < opponent_score:
            print("Du förlorar!")
            winner = opponent_user
            looser = my_team_user

            add_game_to_match_history(my_team_id, opponent_team_id, winner, looser)

            update_points_after_win(winner)
            update_ranking_after_win(winner)

            points_loss = get_user_points()

            return render_template('förlorare.html', points = points_loss, my_score = my_team_score, opponent_score = opponent_score)
            #Andra spelaren får poäng

        else:
            
            print("Vad ska vi göra när det blir lika?")


    return render_template('play_game.html', points=points, teams = teams, my_teams = my_teams)


#My players
@FHL.route('/mina-spelare/')
@flask_login.login_required
def my_players():

    """
    Den inloggade användarens mail sparas i denna: current_user.id. denna används för att ta ut saker ur databasen.
    Hämtar poäng och sedan vilka spelare som användaren har genom get_users_players() med användarens mail som 
    parameter.

    När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
    Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.
    """
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        print("Funktionen kommer att ta lång tid att köra, va 3 min.")
        team_score.insert_score_to_database()

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
    '''
        När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
        Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.
    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)
    points=get_user_points()
    user_id=flask_login.current_user.id

    if len(date_list) < 1:
        print("Hämtar nyare data från API, tar ett tag, var god vänta")
        team_score.insert_score_to_database()

    team_list=database.get_todays_team_list(todaydate, user_id)
    
    if len(team_list) > 0:
        left_forward=database.get_todays_left_forward(todaydate, user_id)
        right_forward=database.get_todays_right_forward(todaydate, user_id)
        list_center=database.get_todays_center(todaydate, user_id)
        left_back=database.get_todays_left_back(todaydate, user_id)
        right_back=database.get_todays_right_back(todaydate, user_id)
        goalkeeper=database.get_todays_goalie(todaydate, user_id)
        return render_template('today_match.html',points=points, left_forward=left_forward, right_forward=right_forward, list_center=list_center, left_back=left_back, right_back=right_back, goalkeeper=goalkeeper, todaydate=todaydate)

    else:
        goalie = get_users_goalie(user_id)
        defenseman = get_users_defenseman(user_id)
        left_wing = get_users_left_wing(user_id)
        center = get_users_center(user_id)
        right_wing = get_users_right_wing(user_id)

        if request.method == 'POST':
            left_forward_form = request.form['left_forward'].split(", ")
            left_forward_id = left_forward_form[0]
            

            center_form = request.form['center'].split(", ")
            center_id = center_form[0]
            

            right_forward_form = request.form['right_forward'].split(", ")
            right_forward_id = right_forward_form[0]
            

            left_defense_form = request.form['left_defense'].split(", ")
            left_defense_id = left_defense_form[0]
            

            right_defense_form = request.form['right_defense'].split(", ")
            right_defense_id = right_defense_form[0]
            

            goalie_form = request.form['goalie'].split(", ")
            goalie_id = goalie_form[0]
            

            team_name = request.form['team_name']

            user_id=flask_login.current_user.id

            add_chosen_players_to_game(left_forward_id, center_id, right_forward_id, left_defense_id, 
            right_defense_id, goalie_id, user_id, team_name)


        return render_template('match.html', points=points, goalie=goalie, defenseman=defenseman, left_wing=left_wing, center=center, right_wing=right_wing)


#Game history
@FHL.route('/match-historik/')
@flask_login.login_required
def match_history():
    points=get_user_points()
    user_id=flask_login.current_user.id

    wins_get = get_wins(user_id)
    losses_get = get_losses(user_id)

    wins = wins_get[1]
    losses = losses_get[1]

    won_games = get_history_won_games(user_id)
    lost_games = get_history_lost_games(user_id)
    

    return render_template('matchhistory.html', points=points, won_games = won_games, lost_games = lost_games, wins=wins, losses=losses)


#Toplist
@FHL.route('/top-spelare')
def top_scorer():
    points=get_user_points()
    '''
    Funktion skickar med sig en lista av lexikon players som hämtad från funktionen get_all_players som finns i 
    database.py. Denna lista sorteras sedan utifrån vad spelarkorten ska sorteras på, exempelvis mål, assist mm.

    När användaren kommer in i filen kollas det i databasen om fhl_players datum är datens datum.
    Om det inte är daten datum körs funktionerna i team_score vilka även uppdaterar tabellen fhl_players med aktuell statistik.
    '''
    todaydate = date.today()
    date_list=database.get_timestamp_fhl_players(todaydate)

    if len(date_list) < 1:
        ("Funktionen kommer att ta lång tid att köra, ca 3 min.")
        team_score.insert_score_to_database()

    players = get_all_players()
    top_players = sorted(players, key = lambda k: k['price'], reverse=True)
    top_players =top_players[:10]
    most_goals = sorted(players, key = lambda k: k['goal'], reverse=True)
    most_goals = most_goals[:10]
    most_assists = sorted(players, key = lambda k: k['assists'], reverse=True)
    most_assists = most_assists [:10]
    most_saves= sorted(players, key = lambda k: k['saves'], reverse=True)
    most_saves=most_saves [:10]
    return render_template('topscorer.html', players = players, top_players = top_players, most_goals = most_goals, most_assists = most_assists, most_saves=most_saves, points=points)


#Forum
@FHL.route('/forum/', methods = ['GET', 'POST'])
@flask_login.login_required
def forum():
    """
    Funktionen visar samtliga foruminlägg
    """
    if request.method == 'POST':
        category = request.form['category']
        points= get_user_points()
        fhldata= get_category_forum(category)
        return render_template('forum.html', points=points, fhldata=fhldata)
    else:
        points= get_user_points()
        fhldata= get_all_forum()
        return render_template('forum.html', points=points, fhldata=fhldata)


#Forum posts created by logged in user
@FHL.route('/forum/mina/inlägg/', methods = ['GET', 'POST'])
@flask_login.login_required
def forum_username():
    """
    Funktionen visas den inloggade användarens foruminlägg
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    fhluserdata = get_forum_username(user_id)
    return render_template('forum_delete.html', points=points, fhluserdata=fhluserdata)


#Forum new post form
@FHL.route('/inlägg/')
@flask_login.login_required
def write_post():
    """
    Functionen låter användaren skapa ett nytt foruminlägg
    """
    points=get_user_points()
    return render_template('write_post.html', points=points)


#Forum new post data
@FHL.route('/form', methods=['POST'])
def form():
    """
    Funktionen sparar ett foruminlägg till databasen
    """
    points=get_user_points()
    user_id=flask_login.current_user.id
    post = post_forum(user_id)
    fhldata = post_forum_redirect()
    return redirect(url_for('forum'))


#Forum delete post
@FHL.route('/forum/mina/inlägg/delete', methods = ['GET', 'POST'])
@flask_login.login_required
def delete_post():
    """
    Funktionen låter använderan ta bort ett foruminlägg
    """
    if request.method == 'POST':
        article_id = request.form['delete']
        delete = delete_article_id(article_id)
        return redirect(url_for('forum_username'))
    else:
        return redirect(url_for('forum_username'))


#Forum like post
@FHL.route('/forum/like', methods = ['GET', 'POST'])
@flask_login.login_required
def forum_like():
    """
    Funktionen låter användare gilla inlägg
    """
    if request.method == 'POST':
        article_id = request.form['like']
        like = like_article_id(article_id)
        points= get_user_points()
        fhldata = get_all_forum()
        return redirect(url_for('forum'))


#Logged in users points
@FHL.route('/points')
@flask_login.login_required
def get_user_points():
    user_id=flask_login.current_user.id
    points=database.get_points(user_id)
    
    for i in points:
        points=i[0]
        
    
    return points

@FHL.route('/vinnare/')
def winner():
    points=get_user_points()
    return render_template('vinnare.html', points=points)

@FHL.route('/förlorare/')
def looser():
    points=get_user_points()
    return render_template('förlorare.html', points=points)


#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)   