from gtts import gTTS 
import playsound
import os

def speak(text): 
	tts = gTTS(text=text, lang='ko') 
	tts.save('voice.mp3') 
	playsound.playsound('voice.mp3')
	os.remove('voice.mp3')

if __name__ == '__main__':
	speak('안녕?')