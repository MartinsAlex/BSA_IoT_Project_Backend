import base64
import os
import requests
import json
import datetime

from flask import Flask, jsonify
from flask import render_template
from utils import createhtmlcurrent, createhtmlforecast, predict_tabular_regression_sample, convert_to_img #call utils file with used functions
from google.cloud import bigquery

app = Flask(__name__, static_folder='files')

LAUSANNE_LATITUDE = 46.52751093142267
LAUSANNE_LONGITUDE = 6.626519003698495


OWM_KEY = os.environ["OWMKEY"][2:] #get keys store in server's OS

@app.route("/")
def hello(name=None):
    return render_template('base.html', name=name)

@app.route("/forecast/")
def forecast():
    #call OWM forcast API
    r_forecast = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()
    createhtmlforecast(r_forecast)
    file = open(os.path.abspath(app.static_folder + '/' + "forecast" + '.png'),'rb') #open img and read it in binary
    data = file.read()
    data = base64.encodebytes(data).decode()
    return jsonify({'msg': 'success', 'img': data}) #send binary with json


@app.route("/current/")
def current():
    r_current = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()
    r_pollution = requests.get(
        f'https://api.openweathermap.org/data/2.5/air_pollution?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={OWM_KEY}').json()

    print(r_current, r_pollution)

    createhtmlcurrent(r_current, r_pollution)
    file = open(os.path.abspath(app.static_folder + '/' + "current" + '.png'),'rb') #open img and read it in binary
    data = file.read()
    data = base64.encodebytes(data).decode()
    return jsonify({'msg': 'success', 'img': data}) #send binary with json

@app.route("/predict/")
def predict_indoor_air_quality():

    BIG_QUERY_CLIENT = bigquery.Client() #connection with bigquery
    #query to retrive last 3000 lines
    query_string = """
        SELECT * FROM `unilbigscaleanalytics.IoT_Project.bme680`
        ORDER BY `timestamp` DESC
        LIMIT 3000
    """
    #create df from the query
    df = (
        BIG_QUERY_CLIENT.query(query_string)
            .result()
            .to_dataframe(
            # Optionally, explicitly request to use the BigQuery Storage API. As of
            # google-cloud-bigquery version 1.26.0 and above, the BigQuery Storage
            # API is used by default.
            create_bqstorage_client=True,
        )
    )
    #calculate means to send in AUTOML
    df['outdoor_temperature_avg_10_min'] = df['outdoor_temperature'].rolling(window=10).mean()
    df['outdoor_humidity_avg_10_min'] = df['outdoor_humidity'].rolling(window=10).mean()
    df['outdoor_air_quality_avg_10_min'] = df['outdoor_air_quality'].rolling(window=10).mean()

    df['outdoor_temperature_avg_1_hour'] = df['outdoor_temperature'].rolling(window=60).mean()
    df['outdoor_humidity_avg_1_hour'] = df['outdoor_humidity'].rolling(window=60).mean()
    df['outdoor_air_quality_avg_1_hour'] = df['outdoor_air_quality'].rolling(window=60).mean()

    df['outdoor_temperature_avg_1_day'] = df['outdoor_temperature'].rolling(window=1440).mean()
    df['outdoor_humidity_avg_1_day'] = df['outdoor_humidity'].rolling(window=1440).mean()
    df['outdoor_air_quality_avg_1_day'] = df['outdoor_air_quality'].rolling(window=1440).mean()

    df = df.iloc[1440:]

    ENDPOINT_ID = "604924909323288576"
    PROJECT_ID = "456026096583"
    LOCATION = "europe-west6"

    instances = [{col: str(df[col].iloc[0]) for col in df.columns}] #create instance to send

    prediction = predict_tabular_regression_sample(
        project=PROJECT_ID,
        endpoint_name=ENDPOINT_ID,
        location=LOCATION,
        instances=instances
    )

    return jsonify(json.loads(prediction)) #return result of automl as JSON

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
