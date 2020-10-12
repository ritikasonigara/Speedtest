from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import func as fn
import json
import os.path
from os import path
import time
import threading

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
def login():
    #TO-DO: enetr the html file name - to be stored in templates folder
    return render_template(".html file ")

@app.errorhandler(Exception)
def handle_exception(e):
    responseDict = {
        "status" : "failure",
        "data" : "exception occured"
    }
    return (json.dumps(responseDict, indent = 4), 400)

@app.route("/currentspeed")
def currentspeed():
    print(request)
    speed = fn.get_new_speeds()
    return (json.dumps(speed))

@app.route('/monitorspeed')
def monitorspeed():
    print(request)
    file_exists = path.exists(fn.filename)
    if (not(file_exists)):
        fn.createfile()
    x = threading.Thread(target=fn.monitor)
    x.start()
    return ""
    
@app.route('/alert',methods = ['POST'])
def send_alert():
    print(request)
    plan = request.values.get('plan')
    value = fn.send_alert(plan)
    return (value)

@app.route('/optimum')
def optimum_time():
    print(request)
    time1,time2 = fn.optimum_time()
    result = time1+" and "+time2
    return result

@app.route('/plot')
def plot():
    print(request)
    if (not(path.exists(fn.filename))):
       time.sleep(1*60) 
    fn.plot_data()
    #TO-DO: enter relative image location below
    return ("loaction  plot image")
    
app.run()