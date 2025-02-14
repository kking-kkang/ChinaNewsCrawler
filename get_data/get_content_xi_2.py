import json
from bs4 import BeautifulSoup
import requests

# JSON 파일 로드
file_path = "../raw_data/raw.people.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 데이터 로드 (리스트 형식)

# 본문 가져오는 함수
def fetch_content(url):
    """
    주어진 URL에서 기사의 본문을 가져옵니다.
    """
    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'  # 인코딩 설정
        if response.status_code != 200:
            print(f"Failed to fetch URL: {url} with status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 주요 본문 추출
        article_div = soup.find('div', class_='detail')
        if not article_div:
            article_div = soup.find('div', id='detail')
        if not article_div:
            article_div = soup.find('div', id='p-detail')
        if not article_div:
            article_div = soup.find('div' ,id='content')
        if not article_div:
            article_div = soup.find('div' ,class_='article')

        if article_div:
            paragraphs = article_div.find_all('p')
            return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

        return None
    except Exception as e:
        print(f"Error fetching content for URL {url}: {e}")
        return None

# 데이터 업데이트
for article in data:  # 리스트 형식으로 순회
    if not article.get('content'):  # content가 없을 경우만 가져오기
        content = fetch_content(article['link'])
        if content:  # 본문이 있을 경우만 업데이트
            article['content'] = content

# JSON 파일 저장
output_path = "./output/add_content_people1.json"
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Updated data saved to {output_path}")
