import base64
import os
import requests
import json

from flask import Flask, jsonify
from flask import render_template
from utils import createhtmlcurrent, createhtmlforecast

app = Flask(__name__, static_folder='files')

LAUSANNE_LATITUDE = 46.52751093142267
LAUSANNE_LONGITUDE = 6.626519003698495

OWM_KEY = os.environ["OWMKEY"][2:]


@app.route("/")
def hello(name=None):
    return render_template('base.html', name=name)

@app.route("/testforecast/")
def testf():
    uri = "https://bsaflaskapp-mdefaecyva-oa.a.run.app/forecast/"
    try:
        uResponse = requests.get(uri)
        
    except requests.ConnectionError:
       return "Connection Error"   

    data = uResponse.json()
    return f'<img src="data:image/png;base64,{data["img"]}">'

@app.route("/testcurrent/")
def testc():
    uri = "https://bsaflaskapp-mdefaecyva-oa.a.run.app/current/"
    try:
        uResponse = requests.get(uri)
        
    except requests.ConnectionError:
       return "Connection Error"   

    data = uResponse.json()
    return f'<img src="data:image/png;base64,{data["img"]}">'

@app.route("/forecast/")
def forecast():
    r_forecast = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()
    createhtmlforecast(r_forecast)
    file = open(os.path.abspath(app.static_folder + '/' + "forecast" + '.png'),'rb')
    data = file.read()
    data = base64.encodebytes(data).decode()
    return jsonify({'msg': 'success', 'img': data})


@app.route("/current/")
def current():
    r_current = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()
    r_pollution = requests.get(
        f'https://api.openweathermap.org/data/2.5/air_pollution?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()

    print(r_current, r_pollution)

    createhtmlcurrent(r_current, r_pollution)
    file = open(os.path.abspath(app.static_folder + '/' + "current" + '.png'),'rb')
    data = file.read()
    data = base64.encodebytes(data).decode()
    return jsonify({'msg': 'success', 'img': data})



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
