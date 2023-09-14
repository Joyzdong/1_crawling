import requests, csv
from bs4 import BeautifulSoup

def crawl_naver():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'}
    url='https://www.melon.com/chart/index.htm'
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    title_list = soup.select('.lst50 .rank01 a')
    title_text_list = [title.text for title in title_list]

    # 주의: titles과는 달리, 가수는 한 노래당 2명 이상이 가능하다는 것까지 고려.
    song_infos = soup.select('#lst50 > td:nth-child(6) > div > div')
    artists_list = [
        song_info.select('div.ellipsis.rank02 > a') for song_info in song_infos]
    artists_text_list = [
        artists[0].text if len(artists)==1
        else (','.join(x.text for x in artists))
        for artists in artists_list]

    csv_list = [('제목', '가수')] + list(zip(title_text_list, artists_text_list))
    with open('melon.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(csv_list)

crawl_naver()