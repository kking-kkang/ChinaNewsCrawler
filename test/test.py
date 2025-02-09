import requests
from bs4 import BeautifulSoup

def fetch_article_content(base_url):
    """
    주어진 기본 URL을 기반으로 여러 페이지에 걸친 기사 본문을 크롤링하여 반환합니다.
    """
    all_content = []
    page_number = 1

    while True:
        # 현재 페이지의 URL 생성
        current_url = f"{base_url}.htm" if page_number == 1 else f"{base_url}_{page_number}.htm"

        try:
            response = requests.get(current_url)
            response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        except requests.RequestException as e:
            print(f"페이지 {page_number} 요청 오류: {e}. 크롤링을 종료합니다.")
            break

        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # id가 'p-detail'인 div 태그 찾기
        content_div = soup.find('div', class_='content')
        if not content_div:
            print(f"페이지 {page_number}: 본문을 포함하는 'div' 태그를 찾을 수 없습니다. 크롤링을 종료합니다.")
            break

        # 모든 p 태그의 텍스트 추출
        paragraphs = content_div.find_all('p')

        # 태그 경우의 수1 -div#p-detail 내부의 p 태그 추출
        #paragraphs = soup.select("div#p-detail p")

        page_content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
        all_content.append(page_content)

        print(f"페이지 {page_number} 크롤링 성공.")
        page_number += 1

    # 모든 페이지의 내용을 하나의 문자열로 결합하여 반환
    return "\n\n".join(all_content)

def extract_base_url(link):
    """
    주어진 링크에서 기본 URL을 추출합니다.
    """
    return link.rsplit('.', 1)[0] if link else ""

url = "http://korea.xinhuanet.com/2016-09/01/c_135650780.htm"
base_url = extract_base_url(url)
article_content = fetch_article_content(base_url)
if article_content:
    print("기사 본문:")
    print(article_content)
else:
    print("기사를 가져올 수 없습니다.")
