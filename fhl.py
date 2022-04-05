#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect


#Application 
FHL = Flask(__name__)


@FHL.route('/')
def index():
    return render_template('index.html')

@FHL.route('/köp-spelare/')
def buy_players():
    return render_template('buy_players.html')

@FHL.route('/forum/')
def forum():
    return render_template('forum.html')

@FHL.route('/guide/')
def guide():
    return render_template('guide.html')

@FHL.route('/login/')
def login():
    return render_template('login.html')

@FHL.route('/match/')
def match():
    return render_template('match.html')

@FHL.route('/match-historik/')
def match_history():
    return render_template('matchhistory.html')

@FHL.route('/mina-spelare/')
def my_players():
    return render_template('my_players.html')

@FHL.route('/registrera/')
def registration():
    return render_template('registration.html')

@FHL.route('/top-spelare')
def top_scorer():
    return render_template('topscorer.html')

@FHL.route('/inlägg/')
def write_post():
    return render_template('write_post.html')


#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)