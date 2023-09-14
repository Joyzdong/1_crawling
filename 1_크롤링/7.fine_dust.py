import requests, csv, json

decoding_key = 'UqUevkUF5pyKUOxLO7bEEesRMdx02SmSkSDTlnLm8NZSKnoTybuV2DAbt/VF8sU66YkK7T7gxRotD9nTjM9WDQ=='
sidoes = ('전국', '서울', '부산', '대구', '인천', '광주', '대전', '울산', '경기', 
	  '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주', '세종')

def record_airinfo(sido):
	if sido not in sidoes: return

	params = {
		'serviceKey': decoding_key,
		'returnType': 'json',
		'numOfRows': '1000',
		'pageNo' : 1,
		'sidoName': sido,
		'ver': '1.0',
	}

	response = requests.get(
		'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty',
		params)
	data = json.loads(response.text)
	airinfos = data['response']['body']['items'] # dictionary list
	record_list = [['시/도명', '동/구명', '미세먼지 수치', '미세먼지 등급', '측정시간']]
	for airinfo in airinfos:
		record_list.append([airinfo['sidoName'], airinfo['stationName'],
							airinfo['pm25Value'], airinfo['pm25Grade'], airinfo['dataTime']])

	with open(f'{sido}_airinfo.csv', 'w', encoding='utf-8-sig', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(record_list)

if __name__ == '__main__':
	record_airinfo('전국')
	record_airinfo('서울')
