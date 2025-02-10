
from serpapi import GoogleSearch
import json

#API_KEY = "3fa81195b3e13146b2c2339cbda3ca2d137914938dc2d1c408a9efbf40e1236b" #지수
#API_KEY = "c4fb69c4f9dd2f679cbe02f56e6a508573e9f7917d07112b8131d241ae2f8c91" #원형
API_KEY = "ff4d975ef5eece46d91dbfe6bb1b0a1b745093e8b7c7b04f25fba59d5f6a7691" #수정
#API_KEY = "65da1190b261bfc7546f5d9494d751d6eb8556bf3d0e9c98520e602b817a7a62" #지영

'''#키워드
query = "site:xinhuanet.com "美日韩""  # 신화통신사
query = "site:people.com.cn "美日韩"" #안민일보  
query = "site:huanqiu.com "美日韩"" #환구시보
query = "site:81.cn "美日韩"" #해방군보
query = "site:ce.cn "美日韩"" #경제일보
query = "site:gmw.cn "美日韩"" #광명일보
'''

# 요청 파라미터 기본 설정
params = {
    "engine": "google",
    "q": 'site:gmw.cn "美日韩"',
    "api_key": API_KEY,
}

results = []  # 전체 결과를 저장할 리스트

try:
    for page in range(0,50 ):
        params["start"] = page * 10  # `pn` 값 설정
        search = GoogleSearch(params)
        response = search.get_dict()

        if "error" in response:
            print(f"오류 발생 (페이지 {page}): {response['error']}")
            break
        elif "organic_results" in response and response["organic_results"]:
            # 필요한 필드만 추출
            for item in response["organic_results"]:
                filtered_result = {
                    "title": item.get("title"),
                    "link": item.get("link"),
                    "date": item.get("date"),
                    "snippet": item.get("snippet"),
                    "source": item.get("source")
                }
                results.append(filtered_result)
            print(f"{page}페이지 결과 수집 완료")
        else:
            print(f"{page}페이지에 검색결과가 없습니다.")
            break

    # 결과를 JSON 파일로 저장
    if results:
        output_file = "raw_data/raw.gmw.json"
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(results, file, ensure_ascii=False, indent=4)
        print(f"검색 결과가 {output_file} 파일로 저장되었습니다.")
    else:
        print("검색결과가 없습니다.")

except Exception as e:
    print(f"요청 중 오류 발생: {e}")
