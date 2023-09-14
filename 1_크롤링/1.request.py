import requests
import json

# get
url = 'https://jsonplaceholder.typicode.com/posts/1'
# 기본적으로 이정도의 예외처리는 해주는 것이 좋음
try:
    response = requests.get(url, timeout=5) # timeout 추가
    response.raise_for_status() # HTTP 응답 코드가 400 이상이라면 HTTPError 발생시킴
except requests.exceptions.Timeout: # timeout 시간안에 응답이 안오면 예외처리
    print("Timeout Error")
except requests.exceptions.ConnectionError: # 연결 자체가 안되는 경우에 대한 예외처리
    print("Error Connecting")
except requests.exceptions.HTTPError: # HTTP 응답 코드가 400 이상인 경우에 대한 에러 처리
    print("Http Error")

json_response = json.loads(response.text)
print(response.text)
print(json_response['title'])


# post
my_post = {'title': '제목', 'body': '내용'}
response = requests.post('https://jsonplaceholder.typicode.com/posts', my_post)
print(response.text)
