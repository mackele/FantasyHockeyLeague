from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error
from datetime import date
from datetime import datetime
import database
import  flask_login 



#Application 
FHL = Flask(__name__)
FHL.secret_key='hej' #ändra senare!

login_manager=flask_login.loginManager()
login_manager.init_app (FHL)


@FHL.route('/login/')
def login():
    return render_template('login.html')