import os
import sys
import requests
import json
from datetime import datetime

from flask import Flask, make_response, send_file, send_from_directory
from flask import render_template

app = Flask(__name__, static_folder='files')

LAUSANNE_LATITUDE = 46.52751093142267
LAUSANNE_LONGITUDE = 6.626519003698495

owmcredits = os.environ["OWMKEY"][2:]
keyconvert = os.environ["CONVKEY"][2:]

@app.route("/")
def hello(name=None):
    return render_template('base.html', name=name, key = keyconvert)


@app.route("/forecast/")
def forecast(name=None):
    r_forecast = requests.get(
        f'http://api.openweathermap.org/data/2.5/forecast?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={owmcredits}').json()
    createhtmlforecast(r_forecast)
    return render_template('tempforecast.html', name=name, forecast=r_forecast)


@app.route("/current/")
def current(name=None):
    LAUSANNE_LATITUDE = 46.52751093142267
    LAUSANNE_LONGITUDE = 6.626519003698495
    r_current = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={owmcredits}').json()
    r_pollution = requests.get(
        f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAUSANNE_LATITUDE}&lon={LAUSANNE_LONGITUDE}&appid={owmcredits}').json()
    print(r_current, sys.stderr)
    createhtmlcurrent(r_current, r_pollution)

    return render_template('tempcurrent.html', name=name)


def createhtmlforecast(data):
    weather = []
    temp = []
    pressure = []
    humidity = []
    wind = []
    for elem in data["list"]:
        if(elem["dt_txt"].split(" ")[1] == "12:00:00"):
            weather.append(elem["weather"][0]["main"])
            temp.append(elem["main"]["temp"])
            pressure.append(elem["main"]["pressure"])
            humidity.append(elem["main"]["humidity"])
            wind.append(elem["wind"]["speed"])

    content = """
        <!DOCTYPE html>
        <html lang="en" class="h-100">

        <head>
            <meta charset="UTF-8">
            <title>Hello World App</title>

            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">

        </head>

        <style>
            .grid-content {
        display: grid;
        grid-template-columns: repeat(5 , minmax(32px, 1fr));
        gap: 2px;
        place-content: center;
        }
        .grid-content div {
        padding: 10px;
        background: #ddd;
        text-align: center;
        }

        </style>

        <body>

            <div class="jumbotron d-flex align-items-center justify-content-center min-vh-100">
                <div class="container-fluid">

                    <div class="row">
                        <div class="col">
                            <div class="card bg-light mx-auto">
                                <div class="card-body">
                                      <h1 class="display-3" style="text-align: center;">Forecast Weather</h1>
                                      <div class="grid-content">
                                        """
    tabday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i in range(0, 5):
        content += "<div><h5>" + tabday[i+1+int(datetime.today().weekday()) % 7] + """</h5>
                    """
        if(weather[i] == "Clouds"):
            content += """<svg width = "50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-2.12393 0 0 2.13534 1576.02-955.55)" x1="393.83" y1="549.46" x2="395.79" y2="542.83"><stop stop-color="#c8e1e8"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="393.83" y1="549.46" x2="390.45" y2="542.88"><stop stop-color="#c3e6ee"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="2" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="396.64" y1="546.11" x2="394.41" y2="538.61"><stop stop-color="#b7d7e1"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><g transform="matrix(1.06658 0 0 1.06658-745.92-181.44)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#2)" transform="matrix(1.21605 0 0 1.21605 343.92-455.87)"/><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#1)" transform="matrix(.7693 0 0 .7693 472.24-205.63)"/><path d="m743.78 199.48c.894-.702 2.02-1.119 3.235-1.119 2.87 0 5.205 2.315 5.279 5.2 2.963 1.124 5.071 4.01 5.071 7.402 0 4-2.942 7.31-6.759 7.831v.072h-27.04v-.013c-3.77-.221-6.759-3.382-6.759-7.25 0-3.73 2.78-6.802 6.36-7.215-.015-.227-.023-.457-.023-.688 0-5.78 4.823-10.466 10.773-10.466 4.404 0 8.19 2.567 9.861 6.245" fill="url(#0)"/></g></svg>"""
        elif(weather[i] == "Clear"):
            content += """<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88" width="50px"><defs><style>.cls-1{fill:#fcdb33;}</style></defs><title>sun-color</title><path class="cls-1" d="M30,13.21A3.93,3.93,0,1,1,36.8,9.27L41.86,18A3.94,3.94,0,1,1,35.05,22L30,13.21Zm31.45,13A35.23,35.23,0,1,1,36.52,36.52,35.13,35.13,0,0,1,61.44,26.2ZM58.31,4A3.95,3.95,0,1,1,66.2,4V14.06a3.95,3.95,0,1,1-7.89,0V4ZM87.49,10.1A3.93,3.93,0,1,1,94.3,14l-5.06,8.76a3.93,3.93,0,1,1-6.81-3.92l5.06-8.75ZM109.67,30a3.93,3.93,0,1,1,3.94,6.81l-8.75,5.06a3.94,3.94,0,1,1-4-6.81L109.67,30Zm9.26,28.32a3.95,3.95,0,1,1,0,7.89H108.82a3.95,3.95,0,1,1,0-7.89Zm-6.15,29.18a3.93,3.93,0,1,1-3.91,6.81l-8.76-5.06A3.93,3.93,0,1,1,104,82.43l8.75,5.06ZM92.89,109.67a3.93,3.93,0,1,1-6.81,3.94L81,104.86a3.94,3.94,0,0,1,6.81-4l5.06,8.76Zm-28.32,9.26a3.95,3.95,0,1,1-7.89,0V108.82a3.95,3.95,0,1,1,7.89,0v10.11Zm-29.18-6.15a3.93,3.93,0,0,1-6.81-3.91l5.06-8.76A3.93,3.93,0,1,1,40.45,104l-5.06,8.75ZM13.21,92.89a3.93,3.93,0,1,1-3.94-6.81L18,81A3.94,3.94,0,1,1,22,87.83l-8.76,5.06ZM4,64.57a3.95,3.95,0,1,1,0-7.89H14.06a3.95,3.95,0,1,1,0,7.89ZM10.1,35.39A3.93,3.93,0,1,1,14,28.58l8.76,5.06a3.93,3.93,0,1,1-3.92,6.81L10.1,35.39Z"></path></svg>"""
        else:
            content += """<svg width = "50" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64"><defs><linearGradient id="8" x1="-512.48" y1="-311.78" x2="-507.41" y2="-333.01" gradientUnits="userSpaceOnUse"><stop stop-color="#ff9300"/><stop offset="1" stop-color="#ffd702"/></linearGradient><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="5" xlink:href="#1" gradientTransform="matrix(.24869.02086-.02071.25039-610.69-323.28)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="7" xlink:href="#1" gradientTransform="matrix(.23788.07548-.07572.23956-547.43-348.62)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="6" xlink:href="#1" gradientTransform="matrix(.24144.06317-.06332.24313-553.91-335.79)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-191.25" x2="-532.77" y1="-184.53" x1="-534.56" id="4" xlink:href="#1"/><linearGradient gradientUnits="userSpaceOnUse" y2="-187.54" x2="-502.64" y1="-178.75" x1="-504.46" id="3" xlink:href="#1"/><linearGradient y2="538.79" x2="394.7" y1="549.38" x1="396.46" gradientUnits="userSpaceOnUse" id="0" xlink:href="#1" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-186.59" x2="-543.45" y1="-177.19" x1="-546.18" id="2" xlink:href="#1"/><linearGradient id="1"><stop stop-color="#7a808a"/><stop offset="1" stop-color="#ced8e0"/></linearGradient></defs><g transform="matrix(.74519 0 0 .74519 412.53 289.83)"><g transform="matrix(1.29586 0 0 1.29586-1506.97-589.71)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#0)" transform="matrix(1.41137 0 0 1.41137 320.53-578.44)"/><g transform="matrix(.66147 0 0 .66147 1114.42 325.53)"><path d="m-542.64-188.14l-4.894 4.727c-1.03 1-1.525 2.509-1.161 4.01.547 2.25 2.815 3.63 5.064 3.083 2.25-.547 3.63-2.815 3.083-5.064l-1.608-6.612c-.053-.218-.323-.297-.485-.141" fill="url(#2)"/><path d="m-502-189.02l-4.143 4.675c-.872.989-1.217 2.405-.777 3.749.661 2.02 2.834 3.122 4.855 2.461 2.02-.661 3.122-2.834 2.461-4.855l-1.942-5.937c-.064-.196-.317-.249-.454-.094" fill="url(#3)"/><path d="m-532.22-192.36l-3.401 3.438c-.716.728-1.043 1.808-.761 2.865.425 1.59 2.058 2.534 3.648 2.109 1.59-.425 2.534-2.058 2.109-3.648l-1.249-4.672c-.041-.154-.234-.206-.347-.092" fill="url(#4)"/><path d="m-538.48-175.91l-1.902 2.776c-.4.587-.492 1.369-.17 2.06.483 1.04 1.712 1.488 2.744 1 1.033-.486 1.478-1.723.995-2.763l-1.419-3.055c-.047-.101-.185-.112-.248-.021" fill="url(#5)"/><path d="m-508.03-178.22l-2.349 2.409c-.495.51-.719 1.264-.521 2 .298 1.107 1.431 1.759 2.532 1.457 1.101-.302 1.752-1.444 1.454-2.551l-.875-3.253c-.029-.107-.163-.142-.24-.063" fill="url(#6)"/><path d="m-509.7-188.91l-2.47 2.286c-.52.484-.783 1.226-.623 1.971.24 1.121 1.339 1.831 2.454 1.585 1.115-.245 1.823-1.353 1.583-2.473l-.707-3.294c-.023-.109-.155-.151-.237-.075" fill="url(#7)"/></g></g><path d="m-507.92-334.43l-9.587 11.662 6.469 3.5-1.676 8.162 9.587-11.662-6.469-3.5z" fill="url(#8)"/></g></svg>"""
        content += """<p><b>Temperature</b><br>""" + str(round(temp[i]-273.15)) + """&#176;C</p>
                    <p><b>Humidity</b><br>""" + str(humidity[i]) + """%</p>
                    <p><b>Wind</b><br>""" + str(wind[i]) + """m/s</p>
                    <p><b>Pressure</b><br>""" + str(pressure[i]) + """ mbar</p> </div>"""
    content += """
                                </div>
                            </div>
                        </div>
                    </div>

                </div>
            </div>


     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>



    </body>

    </html>
    """

    file = open(os.path.abspath(app.static_folder + "/forecast.html"), "w")
    file.write(content)
    file.close()
    convertotimg("forecast")


def createhtmlcurrent(current, pollution):
    no2 = float(pollution["list"][0]["components"]["no2"])
    pm10 = float(pollution["list"][0]["components"]["pm10"])
    o3 = float(pollution["list"][0]["components"]["o3"])
    pm25 = float(pollution["list"][0]["components"]["pm2_5"])
    weather = current["weather"][0]["main"]
    temp = current["main"]["temp"]
    wind = current["wind"]["speed"]
    hum = current["main"]["humidity"]

    pm10_max = 180
    no2_max = 400
    o3_max = 240
    pm2_5_max = 110

    air_quality_index = ((1 - pm10 / pm10_max) + (1 - no2 / no2_max) +
                         (1 - o3 / o3_max) + (1 - pm25 / pm2_5_max)) / 4

    content = """
    
    <!DOCTYPE html>
    <html lang="en" class="h-100">

    <head>
        <meta charset="UTF-8">
        <title>Hello World App</title>

        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
            integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <link href='https://fonts.googleapis.com/css?family=Orbitron' rel='stylesheet' type='text/css'>

    </head>

    <style>

        .clock{
        font-family: 'Orbitron', sans-serif;
        font-size: 7em;
        color: darkblue;
        text-align: center;
    }

        th{
            font-size: larger;
        
        }

        .firstth{
            text-decoration: underline;
        }

        .good{
            color: green;
        }

        .fair{
            color: lightgreen;
        }

        .moderate{
            color : yellowgreen
        }

        .poor{
            color: orange;
        }
        .verypoor{
            color : red;
        }

        tr{
            font-weight: bolder;
            font-size: large;
        }

        td{
            color : darkblue;
        }

        </style>

        <body>

                <div class="jumbotron d-flex align-items-center justify-content-center min-vh-100" style="width : 70%; margin-right : auto; margin-left : auto;">
                    <div class="container-fluid">

                        <div class="row">
                            <div class="col">
                                <div class="card bg-light mx-auto">
                                    <div class="card-body">
                                        <h1 class="display-3" style="text-align: center; margin-bottom: 20px;">Current Weather</h1>
                                        <h1 class="clock">""" + datetime.now().strftime("%H:%M") + """</h1>
                                        <h2>Location : <b style="color : darkblue;">Lausanne (CH)</b> </h2>
                                        
                                        <h4>Long : <i style="color : darkblue;">""" + str(LAUSANNE_LONGITUDE) + """</i><br>Lat : <i style="color : darkblue;">""" + str(LAUSANNE_LATITUDE) + """</i></h4>
                                        <h3 style = "margin-bottom: 10px; margin-top: 10px;">Weather : """
    if(weather == "Clouds"):
        content += """<svg width = "150" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="0" gradientUnits="userSpaceOnUse" gradientTransform="matrix(-2.12393 0 0 2.13534 1576.02-955.55)" x1="393.83" y1="549.46" x2="395.79" y2="542.83"><stop stop-color="#c8e1e8"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="1" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="393.83" y1="549.46" x2="390.45" y2="542.88"><stop stop-color="#c3e6ee"/><stop offset="1" stop-color="#fff"/></linearGradient><linearGradient id="2" gradientUnits="userSpaceOnUse" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)" x1="396.64" y1="546.11" x2="394.41" y2="538.61"><stop stop-color="#b7d7e1"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><g transform="matrix(1.06658 0 0 1.06658-745.92-181.44)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#2)" transform="matrix(1.21605 0 0 1.21605 343.92-455.87)"/><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#1)" transform="matrix(.7693 0 0 .7693 472.24-205.63)"/><path d="m743.78 199.48c.894-.702 2.02-1.119 3.235-1.119 2.87 0 5.205 2.315 5.279 5.2 2.963 1.124 5.071 4.01 5.071 7.402 0 4-2.942 7.31-6.759 7.831v.072h-27.04v-.013c-3.77-.221-6.759-3.382-6.759-7.25 0-3.73 2.78-6.802 6.36-7.215-.015-.227-.023-.457-.023-.688 0-5.78 4.823-10.466 10.773-10.466 4.404 0 8.19 2.567 9.861 6.245" fill="url(#0)"/></g></svg>"""
    elif(weather == "Clear"):
        content += """<svg id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88" width="150px"><defs><style>.cls-1{fill:#fcdb33;}</style></defs><title>sun-color</title><path class="cls-1" d="M30,13.21A3.93,3.93,0,1,1,36.8,9.27L41.86,18A3.94,3.94,0,1,1,35.05,22L30,13.21Zm31.45,13A35.23,35.23,0,1,1,36.52,36.52,35.13,35.13,0,0,1,61.44,26.2ZM58.31,4A3.95,3.95,0,1,1,66.2,4V14.06a3.95,3.95,0,1,1-7.89,0V4ZM87.49,10.1A3.93,3.93,0,1,1,94.3,14l-5.06,8.76a3.93,3.93,0,1,1-6.81-3.92l5.06-8.75ZM109.67,30a3.93,3.93,0,1,1,3.94,6.81l-8.75,5.06a3.94,3.94,0,1,1-4-6.81L109.67,30Zm9.26,28.32a3.95,3.95,0,1,1,0,7.89H108.82a3.95,3.95,0,1,1,0-7.89Zm-6.15,29.18a3.93,3.93,0,1,1-3.91,6.81l-8.76-5.06A3.93,3.93,0,1,1,104,82.43l8.75,5.06ZM92.89,109.67a3.93,3.93,0,1,1-6.81,3.94L81,104.86a3.94,3.94,0,0,1,6.81-4l5.06,8.76Zm-28.32,9.26a3.95,3.95,0,1,1-7.89,0V108.82a3.95,3.95,0,1,1,7.89,0v10.11Zm-29.18-6.15a3.93,3.93,0,0,1-6.81-3.91l5.06-8.76A3.93,3.93,0,1,1,40.45,104l-5.06,8.75ZM13.21,92.89a3.93,3.93,0,1,1-3.94-6.81L18,81A3.94,3.94,0,1,1,22,87.83l-8.76,5.06ZM4,64.57a3.95,3.95,0,1,1,0-7.89H14.06a3.95,3.95,0,1,1,0,7.89ZM10.1,35.39A3.93,3.93,0,1,1,14,28.58l8.76,5.06a3.93,3.93,0,1,1-3.92,6.81L10.1,35.39Z"></path></svg>"""
    else:
        content += """<svg width = "150" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 64 64"><defs><linearGradient id="8" x1="-512.48" y1="-311.78" x2="-507.41" y2="-333.01" gradientUnits="userSpaceOnUse"><stop stop-color="#ff9300"/><stop offset="1" stop-color="#ffd702"/></linearGradient><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="5" xlink:href="#1" gradientTransform="matrix(.24869.02086-.02071.25039-610.69-323.28)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="7" xlink:href="#1" gradientTransform="matrix(.23788.07548-.07572.23956-547.43-348.62)"/><linearGradient gradientUnits="userSpaceOnUse" y2="563.88" x2="0" y1="583.19" id="6" xlink:href="#1" gradientTransform="matrix(.24144.06317-.06332.24313-553.91-335.79)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-191.25" x2="-532.77" y1="-184.53" x1="-534.56" id="4" xlink:href="#1"/><linearGradient gradientUnits="userSpaceOnUse" y2="-187.54" x2="-502.64" y1="-178.75" x1="-504.46" id="3" xlink:href="#1"/><linearGradient y2="538.79" x2="394.7" y1="549.38" x1="396.46" gradientUnits="userSpaceOnUse" id="0" xlink:href="#1" gradientTransform="matrix(2.07793 0 0 2.08909-503.11-599.88)"/><linearGradient gradientUnits="userSpaceOnUse" y2="-186.59" x2="-543.45" y1="-177.19" x1="-546.18" id="2" xlink:href="#1"/><linearGradient id="1"><stop stop-color="#7a808a"/><stop offset="1" stop-color="#ced8e0"/></linearGradient></defs><g transform="matrix(.74519 0 0 .74519 412.53 289.83)"><g transform="matrix(1.29586 0 0 1.29586-1506.97-589.71)"><path d="m311.11 530.14c-.874-.686-1.973-1.095-3.165-1.095-2.808 0-5.093 2.265-5.165 5.087-2.898 1.099-4.961 3.927-4.961 7.241 0 3.916 2.879 7.151 6.613 7.662v.07h26.451v-.013c3.688-.216 6.613-3.309 6.613-7.093 0-3.649-2.72-6.655-6.222-7.06.014-.222.022-.447.022-.673 0-5.655-4.719-10.239-10.539-10.239-4.308 0-8.01 2.512-9.647 6.11" fill="url(#0)" transform="matrix(1.41137 0 0 1.41137 320.53-578.44)"/><g transform="matrix(.66147 0 0 .66147 1114.42 325.53)"><path d="m-542.64-188.14l-4.894 4.727c-1.03 1-1.525 2.509-1.161 4.01.547 2.25 2.815 3.63 5.064 3.083 2.25-.547 3.63-2.815 3.083-5.064l-1.608-6.612c-.053-.218-.323-.297-.485-.141" fill="url(#2)"/><path d="m-502-189.02l-4.143 4.675c-.872.989-1.217 2.405-.777 3.749.661 2.02 2.834 3.122 4.855 2.461 2.02-.661 3.122-2.834 2.461-4.855l-1.942-5.937c-.064-.196-.317-.249-.454-.094" fill="url(#3)"/><path d="m-532.22-192.36l-3.401 3.438c-.716.728-1.043 1.808-.761 2.865.425 1.59 2.058 2.534 3.648 2.109 1.59-.425 2.534-2.058 2.109-3.648l-1.249-4.672c-.041-.154-.234-.206-.347-.092" fill="url(#4)"/><path d="m-538.48-175.91l-1.902 2.776c-.4.587-.492 1.369-.17 2.06.483 1.04 1.712 1.488 2.744 1 1.033-.486 1.478-1.723.995-2.763l-1.419-3.055c-.047-.101-.185-.112-.248-.021" fill="url(#5)"/><path d="m-508.03-178.22l-2.349 2.409c-.495.51-.719 1.264-.521 2 .298 1.107 1.431 1.759 2.532 1.457 1.101-.302 1.752-1.444 1.454-2.551l-.875-3.253c-.029-.107-.163-.142-.24-.063" fill="url(#6)"/><path d="m-509.7-188.91l-2.47 2.286c-.52.484-.783 1.226-.623 1.971.24 1.121 1.339 1.831 2.454 1.585 1.115-.245 1.823-1.353 1.583-2.473l-.707-3.294c-.023-.109-.155-.151-.237-.075" fill="url(#7)"/></g></g><path d="m-507.92-334.43l-9.587 11.662 6.469 3.5-1.676 8.162 9.587-11.662-6.469-3.5z" fill="url(#8)"/></g></svg>"""

    content += """</h3>
                                        <table class="table table-borderless" style="text-align: center;">
                                            <th class = "firstth">Temperature</th>
                                            <th class = "firstth">Wind</th>
                                            <th class = "firstth">Humidity</th>
                                        <tr>
                                            <td > <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-thermometer" viewBox="0 0 16 16">
                                                <path d="M8 14a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3z"/>
                                                <path d="M8 0a2.5 2.5 0 0 0-2.5 2.5v7.55a3.5 3.5 0 1 0 5 0V2.5A2.5 2.5 0 0 0 8 0zM6.5 2.5a1.5 1.5 0 1 1 3 0v7.987l.167.15a2.5 2.5 0 1 1-3.333 0l.166-.15V2.5z"/>
                                            </svg> """ + str(round(temp-273.15)) + """&#176;C</td>
                                            <td > <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-wind" viewBox="0 0 16 16">
                                                <path d="M12.5 2A2.5 2.5 0 0 0 10 4.5a.5.5 0 0 1-1 0A3.5 3.5 0 1 1 12.5 8H.5a.5.5 0 0 1 0-1h12a2.5 2.5 0 0 0 0-5zm-7 1a1 1 0 0 0-1 1 .5.5 0 0 1-1 0 2 2 0 1 1 2 2h-5a.5.5 0 0 1 0-1h5a1 1 0 0 0 0-2zM0 9.5A.5.5 0 0 1 .5 9h10.042a3 3 0 1 1-3 3 .5.5 0 0 1 1 0 2 2 0 1 0 2-2H.5a.5.5 0 0 1-.5-.5z"/>
                                            </svg> """ + str(wind) + """m/s</td>
                                            <td > <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-droplet" viewBox="0 0 16 16">
                                                <path fill-rule="evenodd" d="M7.21.8C7.69.295 8 0 8 0c.109.363.234.708.371 1.038.812 1.946 2.073 3.35 3.197 4.6C12.878 7.096 14 8.345 14 10a6 6 0 0 1-12 0C2 6.668 5.58 2.517 7.21.8zm.413 1.021A31.25 31.25 0 0 0 5.794 3.99c-.726.95-1.436 2.008-1.96 3.07C3.304 8.133 3 9.138 3 10a5 5 0 0 0 10 0c0-1.201-.796-2.157-2.181-3.7l-.03-.032C9.75 5.11 8.5 3.72 7.623 1.82z"/>
                                                <path fill-rule="evenodd" d="M4.553 7.776c.82-1.641 1.717-2.753 2.093-3.13l.708.708c-.29.29-1.128 1.311-1.907 2.87l-.894-.448z"/>
                                            </svg> """ + str(hum) + """%</td>
                                        </tr> 
                                        </table>
                                        <h3>Air Quality :</h3>
                                        <table class="table table-borderless" style="text-align: center;">
                                            <th>NO<sub>2</sub></th>
                                            <th>PM<sub>10</sub></th>
                                            <th>O<sub>3</sub></th>
                                            <th>PM<sub>25</sub></th>
                                            <tr>"""

    for x in range(0, 4):
        content += """<td class="""
        if(x == 0):
            if(no2 < 50):
                content += '"good">GOOD</td>'
            elif(no2 < 100):
                content += '"fair">FAIR</td>'
            elif(no2 < 200):
                content += '"moderate">MODERATE</td>'
            elif(no2 < 400):
                content += '"poor">POOR</td>'
            else:
                content += '"verypoor">VERY POOR</td>'
        elif(x == 1):
            if(pm10 < 25):
                content += '"good">GOOD</td>'
            elif(pm10 < 50):
                content += '"fair">FAIR</td>'
            elif(pm10 < 90):
                content += '"moderate">MODERATE</td>'
            elif(pm10 < 180):
                content += '"poor">POOR</td>'
            else:
                content += '"verypoor">VERY POOR</td>'
        elif(x == 2):
            if(o3 < 60):
                content += '"good">GOOD</td>'
            elif(o3 < 120):
                content += '"fair">FAIR</td>'
            elif(o3 < 180):
                content += '"moderate">MODERATE</td>'
            elif(o3 < 240):
                content += '"poor">POOR</td>'
            else:
                content += '"verypoor">VERY POOR</td>'
        else:
            if(pm25 < 15):
                content += '"good">GOOD</td>'
            elif(pm25 < 30):
                content += '"fair">FAIR</td>'
            elif(pm25 < 55):
                content += '"moderate">MODERATE</td>'
            elif(pm25 < 110):
                content += '"poor">POOR</td>'
            else:
                content += '"verypoor">VERY POOR</td>'

    content += """</tr>
                                        </table>
                                        <br>
                                        <h4>Global air quality : <b style="color : """
    if(round(air_quality_index*100) >= 90):
        content += "green"
    elif(round(air_quality_index*100) >= 80):
        content += "lightgreen"
    elif(round(air_quality_index*100) >= 70):
        content += "yellowgreen"
    elif(round(air_quality_index*100) >= 50):
        content += "orange"
    else:
        content += "red"
    content += """;">""" + str(round(air_quality_index*100)) + """/100</b></h4>
                                    </div>
                                </div>
                            </div>
                        </div>

                    </div>
                </div>


        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>



    </body>

    </html>
    
    """
    file = open(os.path.abspath(app.static_folder + "/current.html"), "w")
    file.write(content)
    file.close()
    convertotimg("current")


def convertotimg(txt):
    instructions = {
        'parts': [
            {
                'html': 'document'
            }
        ],
        "output": {
            "type": "image",
            "format": "png",
            "width": 1024
        }
    }

    response = requests.request(
        'POST',
        'https://api.pspdfkit.com/build',
        headers={
            'Authorization': "Bearer  " + keyconvert
        },
        files={
            'document': open(os.path.abspath(app.static_folder + "/" + txt+".html"), 'rb')
        },
        data={
            'instructions': json.dumps(instructions)
        },
        stream=True
    )

    if response.ok:
        with open(os.path.abspath(app.static_folder + '/' + txt + '.png'), 'wb') as fd:
            for chunk in response.iter_content(chunk_size=8096):
                fd.write(chunk)
    else:
        print(response.text)
    return 1


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
