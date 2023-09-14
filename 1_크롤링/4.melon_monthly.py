import csv, time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.melon.com/chart/month/index.htm')
# 10초안에 웹페이지를 load 하면 바로 넘어가거나, 10초를 기다림.
driver.implicitly_wait(10)

def read_top50list(beautiful = False):
    if beautiful:
        soup = BeautifulSoup(driver.page_source, 'html.parser')   # 파싱하기
        title_list = soup.select('.lst50 .rank01 a')
        title_text_list = [title.text for title in title_list]

        # 주의: titles과는 달리, 가수는 한 노래당 2명 이상이 가능하다는 것까지 고려.
        artists_list = [
            song_info.select('.rank02 > a') for song_info in soup.select('#lst50')]
    else: # selenium
        title_list = driver.find_elements(By.CSS_SELECTOR, '.lst50 .rank01 a')
        title_text_list = [title.text for title in title_list]

        # 주의: titles과는 달리, 가수는 한 노래당 2명 이상이 가능하다는 것까지 고려.
        song_info_list = driver.find_elements(By.CSS_SELECTOR, '#lst50')
        artists_list = [song_info.find_elements(By.CSS_SELECTOR, '.rank02 > a')
                        for song_info in song_info_list]
    
    
    artists_text_list = [artists[0].text if len(artists)==1
                         else (','.join(x.text for x in artists))
                         for artists in artists_list]
    
    return list(zip(title_text_list, artists_text_list))

btn = '#conts > div.calendar_prid > div > button'
# #query 라는 요소가 로딩되어서 나타날때까지 최대 '10초'까지 대기 
# (우리가 찾고자 하는 요소가 나타나면 바로 대기를 중단하고 다음 코드 실행)
# 로딩이 완료되기 전에 요소를 클릭하거나 글을 입력하면 오작동할 수 있으므로, 이를 방지하기 위함
# WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, btn)))

# 월 바꿈 버튼 클릭
driver.find_element(By.CSS_SELECTOR, btn).click()

csv_list= [['제목', '가수']]
month_btns = driver.find_elements(By.CSS_SELECTOR, '.month_calendar a')

for month in range(6):
    month_btns[month].click()
    time.sleep(.5) # 얼마나 슬립할지는 본인 컴퓨터/인터넷 성능에 따라 결정
    csv_list += read_top50list()

with open('melon_monthly.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(csv_list)

driver.quit()
