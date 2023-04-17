import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from difflib import SequenceMatcher
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"

# 페이지 url 형식에 맞게 바꾸어 주는 함수 만들기
# 입력된 수를 1, 11, 21, 31 ...만들어 주는 함수
def make_page_num(num):
    if num == 1:
        return num
    elif num == 0:
        return num + 1
    else:
        return num + 9 * (num - 1)

# 크롤링할 url 생성하는 함수 만들기(검색어, 크롤링 시작 페이지, 크롤링 종료 페이지)
def make_url(search, start_pg, end_pg):
    if start_pg == end_pg:
        start_page = make_page_num(start_pg)
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(start_page)
        print("Generated URL: ", url)
        return [url]
    else:
        urls = []
        for i in range(start_pg, end_pg + 1):
            page = make_page_num(i)
            url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + search + "&start=" + str(page)
            urls.append(url)
        print("Generated URLs: ", urls)
        return urls

# 검색어 입력
search = input("Enter a search keyword:")

# 검색 시작할 페이지 입력
start_pg = int(input("\nEnter the starting page number for the search (e.g. 1, 2, ...):"))
print("\nStarting page: ", start_pg)

# 검색 종료할 페이지 입력
end_pg = int(input("\nEnter the ending page number for the search (e.g. 1, 2, ...):"))
print("\nEnding page: ", end_pg)

# Url 생성 - naver 뉴스
search_urls = make_url(search, start_pg, end_pg)

naver_urls = []
for url in search_urls:
    text = requests.get(url, headers={"User-Agent": USER_AGENT}).text
    naver_urls += list(set(re.findall(r"https://n.news.naver.com/mnews/article/\d+/\d+", text)))

naver_urls = list(set(naver_urls))  # 중복 제거

print("Number of URLs found:", len(naver_urls))

news_data = []

# 이 수정된 코드에서는 scikit-learn의 CountVectorizer 클래스를 사용하여
# 제목과 기존 제목을 토큰 수의 행렬로 변환한 다음 이들 사이의 코사인 유사성을 계산.
# 유사도가 0.7 이상이면 제목을 중복으로 간주하고 콘텐츠 크롤링을 건너뜀.
crawled_titles = []

for url in naver_urls:
    text = requests.get(url, headers={"User-Agent": USER_AGENT}).text
    soup = BeautifulSoup(text, "html.parser")
    title_area = soup.find("h2", {"id": "title_area"})
    if title_area is not None:
        title = title_area.get_text()
        # Compare title similarity with existing titles
        is_duplicate = False
        for existing_title in crawled_titles:
            title_corpus = [existing_title, title]
            vectorizer = CountVectorizer().fit_transform(title_corpus)
            similarity_matrix = cosine_similarity(vectorizer)
            similarity = similarity_matrix[0][1]
            if similarity > 0.7:
                is_duplicate = True
                break
        if not is_duplicate:
            crawled_titles.append(title)
            content_area = soup.find("div", {"class": "newsct_article"})
            if content_area is not None:
                content = content_area.get_text()
            else:
                content = ""
            date_area = soup.find("span", {"class": "t11"})
            if date_area is not None:
                date = date_area.get_text()
            else:
                date = ""
            news_data.append({"title": title, "url": url, "content": content, "date": date})

# 데이터 프레임 생성
news_df = pd.DataFrame(news_data)

# 데이터 프레임 csv file로 생성 및 저장
news_df.to_csv('NaverNews_%s.csv' % search, index=False, encoding='utf-8-sig')

print("Finished")
