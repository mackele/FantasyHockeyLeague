from flask import Flask, render_template, redirect, url_for, request, redirect
import database
import  flask_login 



#Application 
FHL = Flask(__name__)
FHL.secret_key='hej' #ändra senare!

login_manager=flask_login.LoginManager()
login_manager.init_app (FHL)

@FHL.route('/login', methods=['GET', 'POST'])
def login():
    if Flask.request.method == 'GET':
        return Flask.render_tamplate('login.html')

    mail=Flask.request.form['mail']
    password=Flask.request.form['password']
    user=database.login(mail, password) 

    if user>0:
        user=User()
        user.id=mail
        flask_login.login_user(user)
        return Flask.rederect(Flask.url_for('protected'))
    return 'Bad login'

class User (flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(mail):
    if mail not in user:
        return

    user = User()
    user.id = mail
    return user

@FHL.route('/protected')
@flask_login.login_required 
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@FHL.route('/')
def logout():
    flask_login.logout_user()
    return 'logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'unauthorized', 401


@FHL.route('/registration', methods=['GET','POST'])
def registration():
    if Flask.request.method == 'GET':
        return Flask.render_tamplate('login.html')
    
    f_name=Flask.request.form['fname']
    l_name=Flask.request.form['lname']
    mail=Flask.request.form['mail']
    username=Flask.request.form['username']
    password=Flask.request.form['password']
    database.registrations(f_name, l_name, mail, username, password) 

    return Flask.render_template('index.html')
