import json
import re
from datetime import datetime

# 링크에서 날짜 추출 함수
def extract_date_from_link(link):
    try:
        # /YYYY-MM/DD/ 형식을 추출
        match = re.search(r'/(\d{4})/(\d{4})/', link)
        if match:
            # YYYY-MM과 DD를 결합하여 날짜 생성
            raw_date = f"{match.group(1)}{match.group(2)}"  # 예: '20230818'
            # Windows 호환을 위한 0 제거 방식 적용
            formatted_date = datetime.strptime(raw_date, '%Y%m%d').strftime('%b %d, %Y').replace(" 0", " ")
            return formatted_date
        else:
            return None  # 날짜가 없을 경우 None 반환
    except Exception as e:
        print(f"Error extracting date from {link}: {e}")
        return None

# JSON 파일 불러오기
input_file = "../output/filtered_people_add_date.json"
output_file = "../output/filtered_people_add_date.json"

with open(input_file, encoding="utf-8") as file:
    data = json.load(file)

# JSON 데이터에 날짜 적용
if isinstance(data, list):
    for article in data:
        if article.get("date") is None:  # date가 비어 있는 경우
            link = article.get("link", "")
            if link:
                extracted_date = extract_date_from_link(link)
                article["date"] = extracted_date if extracted_date else None

# 업데이트된 JSON 파일 저장
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"작업 완료! 업데이트된 JSON 파일이 저장되었습니다: {output_file}")
