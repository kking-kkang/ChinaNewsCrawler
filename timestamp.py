import json
from datetime import datetime

# JSON 파일 로드
with open("./duplicates.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# 날짜 변환 함수 (YYYY-MM-DD 형식)
def convert_timestamp_to_date(timestamp_ms):
    return datetime.utcfromtimestamp(timestamp_ms / 1000).strftime('%Y-%m-%d')

# JSON 데이터에서 "date" 필드 변환
for item in data:
    if "date" in item and isinstance(item["date"], (int, float)):  # 숫자인 경우만 변환
        item["date"] = convert_timestamp_to_date(item["date"])
    else:
        item["date"] = None  # None 또는 잘못된 값은 None 처리

sorted_data = sorted(data, key=lambda x: x["date"] if x["date"] is not None else "9999-12-31")

# 변환된 JSON을 새 파일로 저장 (선택 사항)
with open("duplicates.json", "w", encoding="utf-8") as file:
    json.dump(sorted_data, file, indent=4, ensure_ascii=False)
