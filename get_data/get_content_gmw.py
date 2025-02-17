import json
from bs4 import BeautifulSoup
import requests
from charset_normalizer import from_bytes

# JSON 파일 로드
file_path = "../output/add_content_gmw3.json"
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)  # JSON 데이터 로드 (리스트 형식)

def detect_encoding(response):
    """
    응답 데이터에서 실제 인코딩을 감지합니다.
    """
    detected = from_bytes(response.content).best()
    return detected.encoding if detected else "utf-8"

# 본문 가져오는 함수
def fetch_content(url):
    """
    주어진 URL에서 기사의 본문을 가져옵니다.
    """
    try:
        response = requests.get(url, timeout=10)

        # 인코딩 감지 및 설정
        encoding = detect_encoding(response)
        response.encoding = encoding

        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch URL: {url} (Status Code: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        # 본문 추출 가능한 HTML 구조 탐색
        article_div = (
                soup.find('div', class_="u-mainText") or
                soup.find('div', id="contentMain") or
                soup.find('div', id='articleContent') or
                soup.find('div', id='ArticleContent') or
                soup.find('article') or
                soup.find('dd', class_="m-con")
        )

        if article_div:
            paragraphs = article_div.find_all('p')
            if paragraphs:
                return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
            else:
                return article_div.get_text(strip=True)
        else:
            paragraphs = soup.find_all('p')  # <p> 태그 전체 탐색
            if not paragraphs:
                print(f"[WARNING] No <p> tags found for URL: {url}")
                return None

            # <p> 태그 내부 <br> 처리
            content = []
            for paragraph in paragraphs:
                for element in paragraph.contents:
                    if element.name == "br":  # <br> 태그는 줄바꿈으로 변환
                        content.append("\n")
                    elif isinstance(element, str):  # 일반 텍스트 추가
                        content.append(element.strip())
                    elif element.name in ["strong", "em"]:  # 강조 태그 텍스트 추가
                        content.append(element.get_text(strip=True))
            return "".join(content)  # 최종 텍스트 조합

    except requests.RequestException as e:
        print(f"[ERROR] Network error while fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for URL {url}: {e}")
        return None

# 데이터 업데이트
for article in data:  # 리스트 형식으로 순회
    if not article.get('content'):  # content가 없을 경우만 가져오기
        content = fetch_content(article['link'])
        if content:  # 본문이 있을 경우만 업데이트
            article['content'] = content
            print(f"[SUCCESS] Content added for URL: {article['link']}")


# JSON 파일 저장
output_path = "../output/add_content_gmw3.json"
with open(output_path, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Updated data saved to {output_path}")
