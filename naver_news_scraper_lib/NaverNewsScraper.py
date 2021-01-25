import pandas as pd
import requests
from bs4 import BeautifulSoup

from datetime import date
import re

class scraper:
    today = re.sub("-",".",date.today().isoformat())
    def __init__(self, title, path, start_date= today, end_date= today):
        self.title = title
        self.start_date = start_date
        self.end_date = end_date
        self.path = path

        self.__start_page = 1
        self.__MAX_NEWS = 10
        self.__COLUMNS = ["title", "date", "press", "contents"] 
        self.__DATA = []

    def naver_news_scraper(self):
        while True:
            # 네이버 뉴스페이지 스크레핑
            url = "https://search.naver.com/search.naver?where=news&query={title}&sm=tab_opt&sort=0&photo=0&field=0&reporter_article=&pd=3&ds={start_date}&de={end_date}&docid=&nso=so%3Ar%2Cp%3Afrom{start_date_except_dot}to{end_date_except_dot}%2Ca%3Aall&mynews=0&refresh_start={start_page}&related=0".format(title= self.title, start_date= self.start_date, end_date= self.end_date, start_date_except_dot= re.sub(".", "", self.start_date), end_date_except_dot= re.sub(".", "", self.end_date), start_page= self.__start_page)
            request = requests.get(url)
            html = BeautifulSoup(request.text, "html.parser")

            # 페이지에 있는 뉴스기사 개수
            amount_news = html.find_all(class_ = "news_area")

            for an in amount_news:
                # 뉴스에 관한 정보
                Press = []
                URL = []
                info = html.find(class_ = "info_group")
                
                # 언론사
                for press in info.find_all("a"):
                    Press.append(press.text)
                    URL.append(press["href"])
                NewsPress = Press[0]

                # 날짜
                SpanData = []
                span = info.find_all("span")
                for sd in span:
                    SpanData.append(sd.text)
                NewsDate = SpanData[-1]
                
                # 네이버 뉴스 URL 추출
                if "네이버뉴스" in info:
                    each_url  = URL[-1]
                    self.each_news_scraper(each_url)

                self.__DATA.append([self.__newstitle, NewsDate, NewsPress, self.__newscontents])

            if amount_news != self.__MAX_NEWS:
                break
            else:
                self.__start_page += 1
        
        # 데이터 저장
        self.save()

    def each_news_scraper(self, url):
        news = requests.get(url, headers={"User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"})
        soup = BeautifulSoup(news.text, "html.parser")

        # 뉴스 제목
        newstitle = soup.find(id = "articleTitle").text

        # 뉴스 본문
        newscontents = soup.find(id = "articleBodyContents").text

        self.__newstitle = newstitle
        self.__newscontents = newscontents

    def save(self):
        df = pd.DataFrame(data = self.__DATA, columns= self.__COLUMNS)
        df.to_csv(self.path + "{name} NaverNewsScap {start} to {end}.csv".format(name = self.title, start = self.start_date, end = self.end_date))