import time
from selenium import webdriver
from selenium.webdriver.common.by import By
def search(key_word):
    deletions = ('검색할래', '검색해 줄래', '검색해줄래', '검색해볼래', '검색해 볼래',
                 '검색해 봐', '검색해봐', '검색해 줘', '검색해줘', '검색해', '검색',
                 '이라고', '라고', '을', '를', '말이야')
    for deletion in deletions:
        key_word = key_word.replace(deletion, '').strip()
    if key_word == '': return

    driver = webdriver.Chrome()
    driver.get('https://naver.com')
    driver.implicitly_wait(10)

    driver.find_element(By.CSS_SELECTOR, '#query').send_keys(key_word)
    driver.find_element(By.CSS_SELECTOR, '#search-btn').click()

    time.sleep(60)
    driver.quit()

if __name__ == '__main__':
    search('안녕')