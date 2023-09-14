############            외부 Library            ############
import speech_recognition as sr
from threading import Thread

############             My module             ############
from common import tts, stt
from word_game import Game
import naver, weather, fine_dust

NAME = '나비'
NAME2 = NAME + ('아' if (ord(NAME[-1]) - 44032) % 28 else '야')
tts.speak(NAME2 + '라고 불러주세요.', False)   # 출력 스레드
print('기다려 주세요..')

############################################################
class Assistant():
    def __init__(self):
        self.is_activated = False
        self.nabi = sr.Recognizer() # 0.00000초
        self.game = Game(self.nabi, winword=True) # 필승단어 끔.

    def listen(self, source):
        while True:
            print('(( 듣는 중 ))' if self.is_activated else '대기 중')
            text = stt.listen(self.nabi, source)
            if text:
                break

        if self.is_activated:
            print(f'<<< {text} >>>')
            return text
        else:
            if NAME2 in text:
                self.is_activated = True
                command = text.split(NAME2)[-1].strip()
                print(f'<<< {NAME2} {command} >>>')
                return command

    def search(self, command):
        Thread(target=naver.search, args=(command,)).start()
        self.is_activated = False

    def weather2(self, command):
        weather.show(command)
        self.is_activated = False

    def finedust(self, command):
        fine_dust.show(command)
        self.is_activated = False

    def wordgame(self, source):
        self.game.play(NAME, source=source)
        self.is_activated = False
        print('\n< 검색, 날씨(도시별), 미세먼지(동/구별), 게임, 자자(종료) >')

    def run(self):
        with sr.Microphone() as source:                     # 0.4초(성능에 따라 변동)
            self.nabi.adjust_for_ambient_noise(source)      # 1.0초
            Thread(target=fine_dust.init).start()           # 마이크 자원 사용후, 미세먼지 초기화 스레드 생성.
            Thread(target=self.game.load_winwords).start()  # 필승 단어 로딩

            print('< 검색, 날씨(도시별), 미세먼지(동/구별), 게임, 자자(종료) >')
            while True:
                command = self.listen(source)
                if not command:
                    continue
                # if '검색' in command:
                #     self.search(command)
                # elif '날씨' in command:
                #     self.weather2(command)
                # elif ('미세' in command) and ('먼지' in command):
                #     self.finedust(command)
                # elif '게임' in command:
                #     self.wordgame(source)
                # elif '자자' in command:
                #     break

                action_phrase = {
                    '검색': [self.search, command],
                    '날씨': [self.weather2, command],
                    '미세먼지': [self.finedust, command],
                    '미세 먼지': [self.finedust, command],
                    '게임': [self.wordgame, source],
                    '자자': [exit, None],
                    }
                ph = action_phrase
                for cmd in action_phrase:
                    if cmd in command:
                        ph[cmd][0](ph[cmd][1])

#################################################################
if __name__ == '__main__':
    assi = Assistant()
    assi.run()
