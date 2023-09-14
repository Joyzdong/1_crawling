import requests, json, os
from bs4 import BeautifulSoup

## 변수 초기화 ##
# 'https://www.data.go.kr/iim/main/mypageMain.do' 에서 decoding_key 복사해오기
url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
params = {
	'serviceKey': os.getenv('decoding_key'),
	'returnType': 'json',
	'numOfRows': '1000',
	'pageNo' : 1,
	'sidoName': '전국',
	'ver': '1.0',
}
sidoes ={'전국':[]}
airinfos = None

###################################################################################
def init():
	response = requests.get(url, params)
	data = json.loads(response.text)
	global airinfos
	airinfos = data['response']['body']['items']
	print('--------------------------------- 미세먼지 정보 등록 완료 ----') # 디버깅 용

def get_current_addr():
	url = 'https://mylocation.co.kr/'
	headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
			'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}

	response = requests.get(url, headers=headers)
	soup = BeautifulSoup(response.text, 'html.parser')
	addr = soup.select('#lbAddr')
	return addr[0].text

def air_info(addr):
	for airinfo in airinfos:
		if airinfo['stationName'] in addr:
			return [airinfo['sidoName'], airinfo['stationName'],
					airinfo['pm25Value'], airinfo['pm25Grade']]
	# 구/동 단위에서 매칭이 안되는 경우 None

def get_air_infos(stations):
	for station in stations:
		for x in airinfos:
			if station == x['stationName']:
				break
		yield air_info(station)

	# station이 없으면 현재주소 사용.
	if not stations:
		yield air_info(get_current_addr())

def show(command):
	stations = [x['stationName'] for x in airinfos if (x['stationName'] in command)]
	infos = get_air_infos(stations)
	for info in infos:
		print(f'{info[0]} {info[1]}, 미세먼지: {info[2]}, 등급: {info[3]}')

##################################################################################
import os
if __name__ == '__main__':
	os.system('cls')

	# sidoes 내용 생성(* 서로 다른 시/도끼리도 중복되는 동/구 없음)
	for x in airinfos:
		sido, station = x['sidoName'], x['stationName']
		if sido in sidoes:
			sidoes[sido].append(station)
		else:
			sidoes[sido] = [station]

	for sido in sidoes:
		print(sido, sidoes[sido], '\n')

