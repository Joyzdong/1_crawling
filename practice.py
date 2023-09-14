import speech_recognition as sr
import time

def callback(recognizer, audio):                          # this is called from the background thread
    try:
        print('...')
        text = recognizer.recognize_google(audio, language = "ko-KR")
        print("You: " + text)  # received audio data, now need to recognize it
    except LookupError:
        print("Oops! Didn't catch that")
    except sr.UnknownValueError:
        print('out')
    except sr.RequestError:
        print('서버 에러 발생')
        exit()

r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
r.listen_in_background(source, callback, phrase_time_limit=5)

print('start')
for i in range(100):
    # print('hello', i)
    time.sleep(1)

