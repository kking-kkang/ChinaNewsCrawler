import pandas as pd

# JSON 파일 불러오기
file_path = "./marge_data_5.json"  # 파일 경로를 맞춰서 사용하세요
df = pd.read_json(file_path)

# "title" 컬럼 기준으로 중복된 값 찾기
duplicates = df[df.duplicated(subset=["title"], keep=False)].sort_values(by=["title"])
unique = df[~df.duplicated(subset=["title"], keep=False)].sort_values(by=["date"])

# 날짜 형식 변환 (ISO 8601 포맷)
if "date" in df.columns:
    duplicates["date"] = pd.to_datetime(duplicates["date"], unit="ms").dt.strftime("%Y-%m-%d")
    unique["date"] = pd.to_datetime(unique["date"], unit="ms").dt.strftime("%Y-%m-%d")

# 결과를 JSON 파일로 저장
duplicates.to_json("./duplicates.json", orient="records", force_ascii=False, indent=4)
unique.to_json("./unique.json", orient="records", force_ascii=False, indent=4)

print("중복된 값들은 duplicates.json 파일에 저장되었습니다.")
print("중복되지 않은 값들은 unique.json 파일에 저장되었습니다.")
