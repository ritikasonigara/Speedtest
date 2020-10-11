import flask
from flask import request
from flask_cors import CORS, cross_origin
import func as fn
import json

app = flask.Flask(__name__)
cors = CORS(app)
app.config['DEBUG'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/currentspeed")
@cross_origin()
def currentspeed():
    speed = fn.get_new_speeds()
    return (json.dumps(speed))

@app.route('/monitorspeed')
@cross_origin()
def monitorspeed():
    plan = request.args.get('plans')
    print(plan)
    #get packspeed from frontend
    fn.createfile()
    fn.monitor(plan)

@app.route('/plot')
@cross_origin()
def plot():
    fn.plot_data()
    return ("C:/Users/rkishore/Desktop/RLL/Backend/image.png")

app.run()