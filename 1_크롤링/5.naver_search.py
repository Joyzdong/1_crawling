import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def naver_search(search_key):
    # 크롬 드라이버 실행 파일이 어디있는지 위치 명시
    # 지금은 같은 경로에 있기 때문에, () 안에 아무것도 명시하지 않아도 무방
    driver = webdriver.Chrome()
    driver.get('https://naver.com')
    driver.implicitly_wait(10)

    # 검색 창에 내용 입력 후 검색 버튼 클릭
    driver.find_element(By.CSS_SELECTOR, '#query').send_keys(search_key)
    driver.find_element(By.CSS_SELECTOR, '#search-btn').click()

    # 잠시 종료 전에 멈추고 검색 잘됐는지 확인
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()   # 브라우저 종료
    
    meanings= soup.select('div.dic_ko p.mean')
    return meanings


if __name__ == '__main__':
    meanings = naver_search('안녕')

    for meaning in meanings:
        print(meaning.text)

        import time



