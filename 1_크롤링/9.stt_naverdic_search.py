import speech_recognition as sr

r = sr.Recognizer()     # 음성 인식 객체

def speech_to_text():
    # 마이크에 담긴 소리를 토대로 아래 코드 실행
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # 잡음 제거 코드 (없어도 무방)
        print('듣는 중...')
        try:
            # 해당 소리를 오디오 파일 형태로 변환
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print('아무 소리도 들리지 않았습니다.')
            return

    print('이해 중...')
    try:
        # 오디오를 토대로 음성 인식(인터넷 연결 필요)
        result = r.recognize_google(audio, language = "ko-KR")
        return result
    except sr.UnknownValueError:
        print("음성 인식 실패")
    except sr.RequestError:
        print('서버 에러 발생')


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://ko.dict.naver.com/')
driver.implicitly_wait(10)

search = speech_to_text()
if search == None: exit()

# 검색 창에 내용 입력 후 검색 버튼 클릭
driver.find_element(By.CSS_SELECTOR, '#ac_input').send_keys(search)
driver.find_element(By.CSS_SELECTOR, '.btn_search').click()

# 잠시 종료 전에 멈추고 검색 잘 됐는지 확인
time.sleep(1)
soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()   # 브라우저 종료

middles = soup.select('#searchPage_entry > div > div:nth-child(1) > ul p')
meanings = []
for middle in middles:
    element = tuple(map(lambda x: x.strip(), middle.text.strip().split('\n')))
    meaning = ' '.join([f'({x})' if i != len(element)-1 else x
                        for i, x in enumerate(element)])
    meanings.append(meaning)

print('검색:', search)

# import pyttsx3  # 음성 지원 module
# engine = pyttsx3.init()
from tts import speak

for meaning in meanings:
    print(meaning)
    
    # engine.say(meaning)
    # engine.runAndWait()
    speak(meaning)
