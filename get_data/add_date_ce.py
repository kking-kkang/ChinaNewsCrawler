import json
import re
from datetime import datetime
import locale

# 로케일 설정 (영어 미국)
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    print("로케일 설정에 실패했습니다. 기본 로케일을 사용합니다.")

# 링크에서 날짜 추출 함수
def extract_date_from_link(link):
    try:
        # /YYYYMM/DD/ 형식의 날짜 추출
        match = re.search(r'/(\d{6})/(\d{2})/', link)  # 예: '/202106/22/'
        if match:
            year_month = match.group(1)  # 'YYYYMM' (예: '202106')
            day = match.group(2)  # 'DD' (예: '22')
            # YYYYMM + DD를 조합하여 'YYYYMMDD' 형식으로 변환
            raw_date = f"{year_month}{day}"  # 예: '20210622'
            # 날짜를 'Jul 1, 2024' 형식으로 변환
            formatted_date = datetime.strptime(raw_date, '%Y%m%d').strftime('%b %d, %Y').replace(" 0", " ")
            return formatted_date
        else:
            return None  # 날짜가 없을 경우 None 반환
    except Exception as e:
        print(f"Error extracting date from link {link}: {e}")
        return None

# JSON 파일 불러오기
input_file = "../output/filtered_ce.json"
output_file = "../output/filtered_ce_add_date.json"

with open(input_file, encoding="utf-8") as file:
    data = json.load(file)

# JSON 데이터에 날짜 적용
if isinstance(data, list):
    for article in data:
        link = article.get("link", "")
        if link:
            extracted_date = extract_date_from_link(link)
            print(f"Link: {link} -> Extracted Date: {extracted_date}")
            article["date"] = extracted_date if extracted_date else None

# 업데이트된 JSON 파일 저장
with open(output_file, "w", encoding="utf-8") as file:
    # ensure_ascii=False로 설정하여 비ASCII 문자를 원래 문자로 저장
    json.dump(data, file, ensure_ascii=False, indent=4)

print(f"작업 완료! 업데이트된 JSON 파일이 저장되었습니다: {output_file}")
