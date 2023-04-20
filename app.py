from flask import Flask, render_template, request
import requests
import mysql.connector
from datetime import date
from keras.models import load_model
# from sklearn.preprocessing import StandardScaler
import numpy as np

# declar l'applicatiom
app = Flask(__name__)

conn = mysql.connector.connect(host="birqavtzyfw7ozkvpelk-mysql.services.clever-cloud.com",
                               user="uavkwsso5m2ibnd3",
                               password="Pd8fcZAbiMD7aE3GlvuH",
                               database="birqavtzyfw7ozkvpelk")
# Ouvrir un curseur pour effectuer des opérations sur la base de données
cur = conn.cursor()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/DATA", methods=['GET', 'POST'])
def data():
    weather_rep = []
    Y = 0.9999

    if request.method == 'POST':
        name = request.form["city"]
        apiKey = "290cd038f745e7a452afc8b5f0d65d7a"
        url = 'http://api.openweathermap.org/data/2.5/forecast?appid='
        lien = url + apiKey + '&q=' + name
        data_city = requests.get(lien).json()
        lat = str(data_city['city']['coord']['lat'])
        lon = str(data_city['city']['coord']['lon'])
        url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&appid=" + apiKey
        data_city3 = requests.get(url2).json()

    for x in data_city3['daily']:
        model = load_model('model.h5')
        X = np.array([[float((x['temp']['day']) - 273.15), float(x['humidity']), float(x['wind_speed']),
                       float(x['wind_deg']), float(x['pop']), Y]])
        IP = model.predict(X)
        Y = float(IP[0, -1])

        weather = [{
            'date': date.fromtimestamp(x['dt']),
            'city': name,
            'temperature': round(((x['temp']['day']) - 273.15), 2),
            'humidity': x['humidity'],
            'wind_speed': x['wind_speed'],
            'wind_degree': x['wind_deg'],
            'preci': x['pop'],
            'IP': Y
        }]
        weather_rep.extend(weather)

        for res in weather:
            cur.execute("INSERT IGNORE INTO data (date, city, temperature, humidity, wind_speed, wind_degree, "
                        "preci) VALUES (%(date)s, %(city)s, %(temperature)s, %(humidity)s, %(wind_speed)s, "
                        "%(wind_degree)s, %(preci)s)", res)
            cur.execute("INSERT IGNORE INTO result (date, city, res) VALUES (%(date)s, %(city)s, %(IP)s)", res)
        conn.commit()
    seuil = 2.5555
    ip_n = 0
    i = 0
    for x in data_city3['daily']:
        model = load_model('model.h5')
        X = [[float((x['temp']['day']) - 273.15), float(x['humidity']), float(x['wind_speed']),
              float(x['wind_deg']), float(x['pop']), Y]]
        IP = model.predict(X)
        Y = float(IP[0, -1])

        ip_n = ip_n + Y
        i += 1
        if ip_n >= seuil:
            a = i
            break
    if ip_n < seuil:
        a = 0

    return render_template('DATA.html', weather_rep=weather_rep,
                           name=name,
                           a=a,
                           )


if __name__ == '__main__':
    app.debug = True
    app.run()
