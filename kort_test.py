#Imported modules 
from flask import Flask, render_template, redirect, url_for, request, redirect
from m import *


#Application 
FHL = Flask(__name__)


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
    players = get_players()
    return render_template('topscorer.html', players = players)


#Forum
@FHL.route('/forum/')
def forum():
    return render_template('forum.html')


#Forum posts
@FHL.route('/inlägg/')
def write_post():
    return render_template('write_post.html')


#Server
FHL.run(host="127.0.0.1", port=8080, debug=True)