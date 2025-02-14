import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
### 환구시보
# JSON 파일 준비
with open("../final.json", encoding="utf-8") as file:
    data = json.load(file)

# 날짜를 추출하는 함수
def get_date_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # 날짜 => class="article-time"
            article_time = soup.find("textarea", class_="article-time")
            if article_time:
                timestamp = int(article_time.text.strip())
                readable_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime('%Y-%m-%d')
                return readable_date
    except Exception as e:
        print(f"Error extracting date from {url}: {e}")
    return None

# 날짜를 "Oct 18, 2024" 형식으로 변환하는 함수
def formatted_date(date):
    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        return date_obj.strftime('%b %d, %Y')  # 'Oct 18, 2024' 형식
    except ValueError as e:
        print(f"Error formatting date {date}: {e}")
        return None

# 널 값 처리
for article in data:
    if article.get("date") is None:  # 날짜가 없는 경우
        url = article.get("link", "")
        if url:
            extracted_date = get_date_from_url(url)
            article["date"] = extracted_date
            # if extracted_date:  # 날짜가 정상적으로 추출되었을 경우만 변환
            #     article["date"] = formatted_date(extracted_date)
            # else:
            #     article["date"] = None  # 날짜를 가져오지 못하면 그대로 None 유지

# 업데이트된 JSON 파일 저장
with open("../final.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("작업 끝")
