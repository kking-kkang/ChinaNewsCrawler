import pandas as pd
import json

# JSON 파일 경로
file_path = "./output/filtered_xinhuanet_by_source.json"

# JSON 파일 로드
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# JSON 데이터를 DataFrame으로 변환
df = pd.DataFrame(data)

# 본문 없는 데이터와 특정 키워드('三边', '三国', '三方', '三角', '同盟')가 포함된 데이터 필터링
df = df[df['content'].notnull() & df['content'].str.contains('三边|三国|三方|三角|同盟', na=False)]

# 소스 통일
df['source'] = '新华网'

# 제목이 중복되는 경우 하나만 유지
df = df.drop_duplicates(subset=['title'], keep='first')

# 필터링된 데이터 저장
output_path = "./output/filtered_xinhuanet_by_source.json"
df.to_json(output_path, orient='records', force_ascii=False, indent=4)

print(f"필터링된 데이터가 '{output_path}'에 저장되었습니다.")
print(df.count())
