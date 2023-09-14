import speech_recognition as sr

r = sr.Recognizer()     # 음성 인식 객체      (약 0.00초 걸림)

def speech_to_text():
    # 마이크에 담긴 소리를 토대로 아래 코드 실행
    with sr.Microphone() as source: #       (약 0.33초 걸림)
        # 잡음 제거 코드 (없어도 무방)
        r.adjust_for_ambient_noise(source) # (약 1초 걸림)
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

if __name__ == '__main__':
    print('결과: ', speech_to_text())
