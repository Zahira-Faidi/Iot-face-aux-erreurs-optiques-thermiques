from keras.models import load_model
from sklearn.preprocessing import StandardScaler
from datetime import date
import requests
import numpy as np

weather_rep = []

Y = 0.999
name = "Casablanca"
apiKey = "290cd038f745e7a452afc8b5f0d65d7a"
url = 'http://api.openweathermap.org/data/2.5/forecast?appid='
lien = url + apiKey + '&q=' + name
data_city = requests.get(lien).json()
lat = str(data_city['city']['coord']['lat'])
lon = str(data_city['city']['coord']['lon'])
url2 = "https://api.openweathermap.org/data/2.5/onecall?lat=" + lat + "&lon=" + lon + "&appid=" + apiKey
data_city3 = requests.get(url2).json()
for x in data_city3['daily']:
    weather = [{
        'date': date.fromtimestamp(x['dt']),
        'temperature': ((x['temp']['day']) - 273.15),
        'humidity': x['humidity'],
        'wind_speed': x['wind_speed'],
        'wind_degree': x['wind_deg'],
        'preci': x['pop'],
        'IP': Y
    }]
    model = load_model('model.h5')
    X = np.array([[float(x['temp']['day']), float(x['humidity']), float(x['wind_speed']), float(x['wind_deg']), float(x['pop']), Y]])
    print(X)
    scaler = StandardScaler()
    tr = scaler.fit_transform(X)
    PI = model.predict(scaler.fit_transform(X))
    print(PI[0, -1])
    Y = PI[0, -1]
    a = date.fromtimestamp()

