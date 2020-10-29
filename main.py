import requests
import json

accuweatherAPIkey = 'Zop2rFzP4JFkQjfKBqQg42oqIEiA5j7j'


def get_coordinates():
    r = requests.get('http://www.geoplugin.net/json.gp')
    if r.status_code == 200:
        location = json.loads(r.text)
        coordinates = {'lat': location['geoplugin_latitude'], 'long': location['geoplugin_longitude']}
        return coordinates
    else:
        return f'Erro ao obter coordenadas.'


def get_location_code(lat, long):
    location_api_url = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey" \
                       "=" + accuweatherAPIkey + "&q=" + lat + "%2C" + long + "&language=pt-br"
    r = requests.get(location_api_url)
    # Se a requisição der erro:
    if r.status_code != 200:
        print('Não foi possível obter o código do local.')
    # Se obter resposta com sucesso:
    else:
        response = json.loads(r.text)
        localInfo = {'city': response['SupplementalAdminAreas'][0]['LocalizedName'],
                     'state': response['AdministrativeArea']['LocalizedName'],
                     'country': response['Country']['LocalizedName'],
                     'locationKey': response['Key']}
        return localInfo


def get_weather_now(local_code, local_name):
    currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + local_code + "?apikey" \
                              "=" + accuweatherAPIkey + "&language=pt-br"
    r = requests.get(currentConditionsAPIUrl)
    if r.status_code == 200:
        currentConditionsResponse = json.loads(r.text)
        weather_info = {'weatherText': currentConditionsResponse[0]['WeatherText'],
                        'temperature': currentConditionsResponse[0]['Temperature']['Metric']['Value'],
                        'localName': local_name}
        return weather_info
    else:
        print(r.status_code)
        print('Não foi possível obter o código do local.')


# Beggins

coordinates = get_coordinates()
local = get_location_code(coordinates['lat'], coordinates['long'])
weather_conditions = get_weather_now(local['locationKey'], local['city'])

print(f'Clima atual em: {weather_conditions["localName"]}')
print(f'Temperatura {weather_conditions["temperature"]} ºC')
print(f'Condição climática: {weather_conditions["weatherText"]}')


