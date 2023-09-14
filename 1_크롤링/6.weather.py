import requests, json, time

# 도시별 (위도, 경도)
pos = {'Seoul': (37.566,126.9784), 'London':(51.5085,-0.1257),
       'New York':(40.7143,-74.006)}
weather={0:'매우 맑음', 1:'맑음', 2:'약간 흐림', 3:'흐림', 80:'Rain showers: Slight',
         81:'Rain showers: moderate', 82:'Rain showers: violent',
         61:'Rain: Slight', 63:'Rain: moderate', 65:'Rain: heavy intensity'}

def show_weather(city):
    response = requests.get(
        f'https://api.open-meteo.com/v1/forecast?latitude={pos[city][0]}'
        f'&longitude={pos[city][1]}&current_weather=true&timezone=auto')
    data = json.loads(response.text)

    print(f"[{city:^10}] {data['current_weather']['temperature']}°C", end=', ')
    try:
        print(weather[data['current_weather']['weathercode']], end=', ')
    except:
        print(data['current_weather']['weathercode'])
        print('Update weather code!')
        print('find code here. https://open-meteo.com/en/docs')
    print(f"{data['current_weather']['windspeed']}km/h")

print(time.strftime("<%Y-%m-%d, %H시> 현재", time.localtime()))
for city in pos:
    show_weather(city)
    
