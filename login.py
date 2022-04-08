from flask import Flask, render_template, redirect, url_for, request, redirect
import psycopg2
from psycopg2 import Error
from datetime import date
from datetime import datetime
from  flask_login 


#Application 
FHL = Flask(__name__)

