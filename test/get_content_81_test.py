import requests
from bs4 import BeautifulSoup, Comment
from charset_normalizer import from_bytes

def detect_encoding(response):
    """
    응답 데이터에서 실제 인코딩을 감지합니다.
    """
    detected = from_bytes(response.content).best()
    return detected.encoding

def fetch_content_with_comments(url):
    """
    주어진 URL에서 HTML 주석 안의 본문을 포함하여 가져옵니다.
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

        # <div id="APP-Content"> 찾기
        article_div = soup.find('div', id='APP-Content')
        if article_div:
            # HTML 주석 처리된 내용 추출
            comments = article_div.find_all(string=lambda text: isinstance(text, Comment))
            extracted_text = ""
            for comment in comments:
                # 주석 내부 파싱
                comment_soup = BeautifulSoup(comment, 'html.parser')
                paragraphs = comment_soup.find_all('p')
                extracted_text += "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])

            if extracted_text.strip():
                return extracted_text.strip()
            else:
                return article_div.get_text(strip=True)
        else:
            print(f"[WARNING] No valid article div found for URL: {url}")
            return None

    except requests.RequestException as e:
        print(f"[ERROR] Network error while fetching URL {url}: {e}")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for URL {url}: {e}")
        return None

# 테스트 URL
url = "http://www.81.cn/jfjbmap/content/2022-04/12/content_313419.htm"

# 본문 가져오기
content = fetch_content_with_comments(url)

# 결과 출력
if content:
    print("[SUCCESS] Extracted Content:")
    print(content)
else:
    print("[FAILURE] No content extracted.")
