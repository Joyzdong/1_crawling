import requests, csv
from bs4 import BeautifulSoup

def crawl_naver(category, date, page):
    # requests 모듈을 통해서 요청보내고, html 문서받기
    headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    url = f'https://news.naver.com/main/list.naver?mode=LSD&mid=sec&sid1={category}&date={date}&page={page}'
    response = requests.get(url, headers=headers)


    # 파싱하기
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = [['제목', '본문', '신문사', '작성시각']]
    # 원하는 정보 선택하기
    news_list = soup.select('.type06_headline > li')
    for news in news_list:
        title = news.select('a')[-1].text.strip()
        content = news.select('.lede')[0].text
        writer = news.select('.writing')[0].text
        date = news.select('.date')[0].text

        rows.append([title, content, writer, date])
        
    with open('news.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

crawl_naver(103, 20230101, 1)

