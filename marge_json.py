import json

# 두 개의 JSON 파일 로드
with open("./output/raw.81.json", "r", encoding="utf-8") as file:
    json_file1 = json.load(file)

with open("./output/raw.81-1.json", "r", encoding="utf-8") as file:
    json_file2 = json.load(file)

# 두 개의 리스트를 하나로 합침
merged_data = json_file1 + json_file2

# 합친 데이터를 새로운 JSON 파일로 저장
with open("./output/raw.81.json", "w", encoding="utf-8") as file:
    json.dump(merged_data, file, ensure_ascii=False, indent=4)

