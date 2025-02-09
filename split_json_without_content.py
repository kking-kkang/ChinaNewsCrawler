import json
import pandas as pd

# JSON 파일 로드
file_path = "output/add_content_without_ce.json"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# "content" 컬럼이 있는 항목과 없는 항목으로 분리
with_content = [entry for entry in data if "content" in entry]
without_content = [entry for entry in data if "content" not in entry]

# 결과를 JSON 파일로 저장
with open("output/add_content_without_ce.json", "w", encoding="utf-8") as file:
    json.dump(with_content, file, ensure_ascii=False, indent=4)

with open("./output/ce_pdf.json", "w", encoding="utf-8") as file:
    json.dump(without_content, file, ensure_ascii=False, indent=4)


