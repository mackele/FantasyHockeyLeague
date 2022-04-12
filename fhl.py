#Imported modules 
from operator import truediv
from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error
from datetime import date
from datetime import datetime
import database
import  flask_login 
import hashlib


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
@flask_login.login_required
def index():
    return render_template('index.html')


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

@FHL.route('/protected')
@flask_login.login_required 
def protected():
    return render_template('index.html')

#logga ut 
@FHL.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('unauthorized_index.html')

#index för icke inloggade
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized_index.html')


# registration
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
    
    return render_template('login.html')


#Guide
@FHL.route('/guide/')
def guide():
    return render_template('guide.html')


#Buy players
@FHL.route('/köp-spelare/')
@flask_login.login_required
def buy_players():
    return render_template('buy_players.html')


#My players
@FHL.route('/mina-spelare/')
@flask_login.login_required
def my_players():

    """
    den inloggade användarens mail sparas i denna: current_user.id. denna används för att ta ut saker ur databasen.
    """
    return render_template('my_players.html')


#Game
@FHL.route('/match/')
@flask_login.login_required
def match():
    return render_template('match.html')


#Game history
@FHL.route('/match-historik/')
@flask_login.login_required
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
@flask_login.login_required
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