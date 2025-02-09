import requests
from bs4 import BeautifulSoup
import json


def fetch_article_content(base_url):
    all_content = []
    page_number = 1

    while True:
        # 현재 페이지에 대한 URL 생성
        if page_number == 1:
            current_url = f"{base_url}.htm"
        else:
            current_url = f"{base_url}_{page_number}.htm"

        # 요청 보내기
        try:
            response = requests.get(current_url)
            response.raise_for_status()  # HTTP 오류 발생 시 예외
        except requests.RequestException as e:
            print(f"페이지 {page_number} 요청 오류: {e}. 종료.")
            break

        if response.status_code == 200:
            # HTML 내용 파싱
            soup = BeautifulSoup(response.text, 'html.parser')

            # div#p-detail 내부의 p 태그 추출
            paragraphs = soup.select("div#p-detail p")
            if not paragraphs:
                print(f"페이지 {page_number}: 본문 없음. 종료.")
                break

            # 문단 텍스트 수집
            page_content = "\n".join([p.get_text().strip() for p in paragraphs])
            all_content.append(page_content)

            print(f"페이지 {page_number} 크롤링 성공.")
            page_number += 1
        else:
            print(f"페이지 {page_number} 로드 실패: {response.status_code}. 종료.")
            break

    # 모든 내용을 하나의 기사로 결합
    full_article = "\n\n".join(all_content)

    # 불필요한 줄 필터링
    filtered_article = "\n".join(
        line for line in full_article.splitlines()
        if not any(x in line for x in ["上一页", "下一页", "新华国际今日排行榜", "全球动物袭击游客", "拜神社入钓岛", "美爆炸案"])
    )

    # 연속된 공백 줄 이후 내용 제거
    lines = filtered_article.splitlines()
    cleaned_lines = []
    empty_line_count = 0

    for line in lines:
        if line.strip() == "":
            empty_line_count += 1
        else:
            empty_line_count = 0

        if empty_line_count >= 3:
            break

        cleaned_lines.append(line)

    # 정리된 기사 반환
    return "\n".join(cleaned_lines)


def extract_base_url(link):
    """
    주어진 링크에서 기본 URL 추출
    """
    if not link:
        return ""
    # ".htm" 제거
    return link.split(".htm")[0]


def add_article_content_to_json(json_data):
    """
    JSON 데이터에서 각 기사에 본문을 추가
    """
    for article in json_data:  # 리스트의 각 기사를 처리
        base_url = extract_base_url(article.get("link", ""))
        if base_url:
            print(f"URL 본문 가져오는 중: {base_url}")
            article["content"] = fetch_article_content(base_url)
        else:
            article["content"] = ""
    return json_data


# JSON 파일 읽기
with open("./output/test_xinhuanet.json", encoding="utf-8") as file:
    data = json.load(file)  # JSON 데이터를 리스트로 로드

# 데이터 처리
updated_data = add_article_content_to_json(data)

# 결과 저장
with open("./output/xinhuanet.json", "w", encoding="utf-8") as outfile:
    json.dump(updated_data, outfile, ensure_ascii=False, indent=4)

print("데이터 저장 완료")
