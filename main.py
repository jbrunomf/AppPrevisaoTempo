import requests
import json
import pprint

accuweatherAPIkey = 'Zop2rFzP4JFkQjfKBqQg42oqIEiA5j7j'
# locationKey = "44157"
r = requests.get('http://www.geoplugin.net/json.gp')

if r.status_code == 200:
    location = json.loads(r.text)
    longitude = location['geoplugin_longitude']
    latitude = location['geoplugin_latitude']
    # print(f'Latitude: {latitude} Longitude: {longitude}')
    locationAPiUrl = "http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey" \
                     "="+accuweatherAPIkey+"&q="+latitude+"%2C"+longitude+"&language=pt-br"

    r2 = requests.get(locationAPiUrl)
    if r.status_code != 200:
        print('Não foi possível obter o código do local.')
    else:
        response = json.loads(r2.text)
        state = response['AdministrativeArea']['LocalizedName']
        country = response['Country']['LocalizedName']
        city = response['SupplementalAdminAreas'][0]['LocalizedName']
        locationKey = response['Key']
        print(f'Cidade: {city} Estado: {state} País: {country} Código do local (Accuweather): {locationKey}')

        currentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/"+locationKey+"?apikey" \
                                  "="+accuweatherAPIkey+"&language=pt-br"
        r3 = requests.get(currentConditionsAPIUrl)
        if r3.status_code == 200:
            currentConditionsResponse = json.loads(r3.text)
            weatherText = currentConditionsResponse[0]['WeatherText']
            temperature = currentConditionsResponse[0]['Temperature']['Metric']['Value']
            print(f'A temperatura atual é: {temperature} ºC, Condição climática: {weatherText}')
        else:
            print(r3.status_code)
            print('Não foi possível obter o código do local.')
else:
    print('Não foi possível obter a localização.')


