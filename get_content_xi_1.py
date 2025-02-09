import requests
from bs4 import BeautifulSoup
import json

def fetch_article_content(base_url):
    """
    주어진 URL에서 여러 페이지를 크롤링하여 기사 본문을 반환.
    """
    all_content = []
    page_number = 1

    while True:
        current_url = f"{base_url}.htm" if page_number == 1 else f"{base_url}_{page_number}.htm"

        try:
            response = requests.get(current_url)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"❌ 페이지 {page_number} 요청 오류: {e}. 크롤링 종료.")
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        # 본문을 포함할 가능성이 있는 태그 찾기
        content_div = soup.find('div', class_='content') or soup.find('span', id='content')

        if not content_div:
            print(f"⚠️ 페이지 {page_number}: 본문을 포함하는 태그를 찾을 수 없음. 크롤링 종료.")
            break

        paragraphs = content_div.find_all('p')
        if not paragraphs:
            print(f"⚠️ 페이지 {page_number}: 본문이 없음. 크롤링 종료.")
            break

        # 문단 텍스트 수집
        page_content = "\n".join([p.get_text().strip() for p in paragraphs])
        all_content.append(page_content)

        print(f"✅ 페이지 {page_number} 크롤링 성공.")
        page_number += 1

    return "\n\n".join(all_content) if all_content else None

def extract_base_url(link):
    return link.split(".htm")[0] if link else ""

def add_article_content_to_json(json_data):
    for entry in json_data:
        link = entry.get("link")
        if link:
            base_url = extract_base_url(link)
            print(f"🔍 본문 가져오는 중: {base_url}")
            article_content = fetch_article_content(base_url)

            # 기존 'content'가 있으면 유지하고, 새로 크롤링한 본문이 있으면 덮어쓰기
            if article_content:
                entry["content"] = article_content
            elif "content" in entry and entry["content"]:
                print(f"🔄 기존 content 유지: {entry['content'][:30]}...")  # 기존 본문 유지 로그

    return json_data

# JSON 파일 읽기
input_file = "./output/add_content_xinhuanet3.json"
output_file = "./output/add_content_xinhuanet4.json"

with open(input_file, encoding="utf-8") as file:
    data = json.load(file)

# 데이터 처리
updated_data = add_article_content_to_json(data)

# 결과 저장
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(updated_data, outfile, ensure_ascii=False, indent=4)

