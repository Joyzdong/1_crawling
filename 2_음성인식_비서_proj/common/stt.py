import speech_recognition as sr

def listen(recognizer, source) -> str:
    try:
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        print('...')
        text = recognizer.recognize_google(audio, language="ko-KR")
    except sr.WaitTimeoutError:
        # 아무 소리도 들리지 않은 경우
        return ''
    except sr.UnknownValueError:
        # 이해 안되는 소리 무시하기
        return ''
    except sr.RequestError:
        print('서버 에러 발생')
        exit()
    return text
