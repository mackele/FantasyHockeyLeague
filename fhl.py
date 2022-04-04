#Imported modules 
from flask import Flask, render_template, request, redirect


#Application 
FHL = Flask(__name__)


@FHL.route('/')
def index():
    return render_template('index.html')







#Server 
FHL.run(host="127.0.0.1", port=8080, debug=True)