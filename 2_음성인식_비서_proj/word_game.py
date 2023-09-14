import requests, json, os
from common import tts, stt

## 초기화 변수
# 'https://opendict.korean.go.kr/service/openApiRegister' 에서 key 복사해오기
url = 'http://opendict.korean.go.kr/api/search'

# 상수관리
GIVING_UP = '게임포기'
MUST_WIN_LETTER = {'료', '률', '름', '츠', '갗', '륨', '력', '류', '령', '례', '련',
                   '략', '릇', '쁨', '션', }
WIN_LETTER = {'럽', '슘', '량', '륙', '즘', '듬', }

class Game:
    def __init__(self, nabi=None, source=None, winword=True):
        self.params = {
            'key': os.getenv('key'),
            'q': '',
            'req_type': 'json',
            'num': 100,
            'advanced': 'y',
            'type1': ['word'],
            'type3': ['general'],
            'type4': ['general'],
            'pos': [1],  # 명사
            'letter_s': 2,
            'sort': 'popular',
            'method': 'exact',
            }
        self.words = []
        self.nabi = nabi
        self.source = source
        self.use_winword = winword
        self.mustwin_words = []
        self.win_words = []

    def load_winwords(self):
        if not self.use_winword:
            return

        for letter in MUST_WIN_LETTER:
            data = self.receive(letter, method='end')
            for item in data['channel']['item']:
                self.mustwin_words.append(item['word'])
        for letter in WIN_LETTER:
            data = self.receive(letter, method='end')
            for item in data['channel']['item']:
                self.win_words.append(item['word'])
        print('-------------------------------------필승단어 로딩완료----') # 디버깅 용

    def receive(self, text, method):
        self.params.update({'q': text, 'method': method})

        try:
            response = requests.get(url, self.params, timeout=5)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Timeout Error")
        except requests.exceptions.ConnectionError as e:
            print(e, "Error Connecting")
            exit()
        except requests.exceptions.HTTPError:
            print("Http Error")
        except Exception as e:
            print(e)
            exit()

        return json.loads(response.text)

    def verify(self, word):
        if not word:    # word == None 일때 탈락.
            return False

        print(f'<<< USER: {word} >>> ', end='')
        if self.words and (self.words[-1][-1] != word[0]):
            print(f'끝말: {self.words[-1][-1]}')
            tts.say('끝말을 이어 주세요.')
            return False
        else:
            print()

        if len(word) < 2:
            tts.say('두 글자 이상 말해 주세요.')
            return False
        elif word in self.words:
            tts.say("이미 말했던 단어입니다.")
            return False

        data = self.receive(word, method='exact')
        if data['channel']['num'] == 0:
            tts.say('없는 단어입니다.')
            return False
        else:
            self.words.append(word)
            return True

    def user_turn(self):
        while True:  # word를 얻을 때까지 반복
            print('(( 단어 듣는 중 ))')
            word = stt.listen(self.nabi, self.source)
            word = word.replace(' ', '')
            if GIVING_UP in word:
                return GIVING_UP

            if self.verify(word):
                return

    def find_win_word(self, NAME):
        word = ''
        data = self.receive(self.words[-1][-1], method='start')
        for item in data['channel']['item']:
            if len(item['word']) < 2:
                continue  # 한 글자 단어 패스
            elif item['word'] in self.words:
                continue  # 이미 말했던 단어 패스

            if not word:
                word = item['word']
            if (item['word'] in self.mustwin_words) or (item['word'] in self.win_words):
                word = item['word']     # 필승단어 or 승리단어 선택
                self.words.append(word)
                print(f'<<< {NAME}: {word} >>>')
                tts.speak(word)
                return word
            else:
                continue
        else:
            return word

    def ai_turn(self, NAME):
        last_len = len(self.words)
        word = self.find_win_word(NAME)
        if len(self.words) > last_len:
            return

        if word:
            self.words.append(word)
            print(f'<<< {NAME}: {word} >>>')
            tts.speak(word)
            return
        else:
            return GIVING_UP

    def play(self, NAME, nabi=None, source=None):
        if nabi: self.nabi = nabi
        if source: self.source = source

        NAME2 = NAME + ('이' if (ord(NAME[-1]) - 44032) % 28 else '가')
        tts.say('게임을 시작합니다. 단어를 말해주세요.')
        while True:
            if self.user_turn() == GIVING_UP:
                tts.say(NAME2 + ' 이겼습니다.')
                return

            if self.ai_turn(NAME) == GIVING_UP:
                tts.say('당신의 승리입니다.')
                return

######################################################################
import speech_recognition as sr

if __name__ == '__main__':
    game = Game()

    text = '듬'
    data = game.receive(text, method='end')
    for item in data['channel']['item']:
        # print(item)
        print(item['word'])

    ## tts.speak(word) 에서 에러남!!
    # nabi = sr.Recognizer()  # 0.00000초
    # with sr.Microphone() as source:             # 0.4초(성능에 따라 변동)
    #     nabi.adjust_for_ambient_noise(source)   # 1.0초
    #     game.play(nabi, source)

