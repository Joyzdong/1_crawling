import requests, json

# 도시별 (위도, 경도)
pos = {'서울': (37.566, 126.9784), '부산': (35.1017, 129.03), '전주': (35.8219, 127.1489),
       '대전': (36.3491, 127.3849), '대구': (35.8703, 128.5911), '광주': (35.1547, 126.9156),
       '인천': (37.4565, 126.7052), '강릉': (37.7527, 128.8724), '춘천': (37.8747, 127.7342),
       '수원': (37.2911, 127.0089), '성남': (37.4386, 127.1378),
       '런던': (51.5085,-0.1257), '뉴욕': (40.7143,-74.006),
       }
weather={
    0:'매우 맑음', 1:'맑음', 2:'약간 흐림', 3:'흐림',
    80:'소낙비: Slight', 81:'소낙비: moderate', 82:'소낙비: violent',
    61:'비: Slight', 63:'비: moderate', 65:'비: heavy',
    51:'이슬비: Light', 53:'이슬비: moderate', 55:'이슬비: dense',
    }

def set_pos(city):
    if city in pos: return
    # 위치 얻어와서 pos에 저장.

# url='https://open-meteo.com/en/docs#api_form' # 날씨 사이트
def get_data(city):
    response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={pos[city][0]}&'
                            f'longitude={pos[city][1]}&current_weather=true&windspeed_unit=ms')
    return json.loads(response.text)

def show(text):
    cities = [city for city in pos if city in text]
    if not cities: cities.append('서울')

    for city in cities:
        data = get_data(city)

        print(f"[{city:^10}] {data['current_weather']['temperature']}°C", end=', ')
        try:
            print(weather[data['current_weather']['weathercode']], end=', ')
        except:
            print(data['current_weather']['weathercode'])
            print('Update weather code!')
            print('find code here. https://open-meteo.com/en/docs')
        print(f"{data['current_weather']['windspeed']}m/s")

##################################################################################
import time

if __name__ == '__main__':
    print(time.strftime("<%Y-%m-%d, %H시> 현재", time.localtime()))
    for city in pos:
        show(city)