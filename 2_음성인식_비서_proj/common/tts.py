from gtts import gTTS
import playsound, os

# block=False 일 때, 0.35초 정도의 cost가 든다.
def speak(text, block=True):
	tts = gTTS(text=text, lang='ko')
	tts.save('voice.mp3')
	playsound.playsound('voice.mp3', block)
	os.remove('voice.mp3')


#################################################
import pyttsx3
engine = pyttsx3.init()

def say(text):
	engine.say(text)
	engine.runAndWait()


#################################################
if __name__ == '__main__':
	msg = '끝말잇기 게임을 하자'
	speak(msg)
	say(msg)