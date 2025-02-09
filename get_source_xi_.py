import json
from bs4 import BeautifulSoup
import requests

# JSON 파일 로드
file_path = "./output/filtered_people.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 데이터 로드 (리스트 형식)

# 소스 가져오는 함수
def fetch_source(url):
    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"Failed to fetch URL: {url} with status code {response.status_code}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 소스 추출
        source_div = (
            soup.find('div', class_='source') or
            soup.find('div', class_='name_nolink') or
            soup.find('em', id='source') or
            soup.find('span', id='source') or
            soup.find('a', class_='name') or
            soup.find('span', string=lambda t: '来源' in t if t else False)
        )

        if source_div:
            return source_div.text.strip()  # 텍스트 추출 후 반환
        else:
            print(f"No source found for URL: {url}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request error for URL {url}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching content for URL {url}: {e}")
        return None

# 데이터 업데이트
for article in data:  # 리스트 형식으로 순회
    if not article.get('get_source'):  # get_source 필드가 없거나 None이면 가져오기
        get_source = fetch_source(article['link'])
        if get_source:  # 본문이 있을 경우만 업데이트
            article['get_source'] = get_source

# JSON 파일 저장
output_path = "./output/add_content_source_people1.json"
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Updated data saved to {output_path}")
