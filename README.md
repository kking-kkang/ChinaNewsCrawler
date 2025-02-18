# 국제관계 분석 과정

# 중국기사  수집 과정

![그림2.png](%E1%84%80%E1%85%AE%E1%86%A8%E1%84%8C%E1%85%A6%E1%84%80%E1%85%AA%E1%86%AB%E1%84%80%E1%85%A8%20%E1%84%87%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%E1%86%A8%20%E1%84%80%E1%85%AA%E1%84%8C%E1%85%A5%E1%86%BC%201819d1de3e06805f96d7e0d18212ea11/%EA%B7%B8%EB%A6%BC2.png)

## Step 1 -Basic Crawling

구글검색을 이용해 **언론사 별로** **美日韩 키워드**로  기사의 raw data(title, url, date) 수집

이때, date 값이 존재하는 경우도 있고 없는 경우도 있음

`site:xinhuanet.com "美日韩"` → 신화사 기사만 검색

`site:people.com.cn "美日韩"` → 인민일보 기사만 검색

`site:globaltimes.cn "美日韩"` → 환구시보 기사만 검색

데이터 수 확보를 위해 언론사 추가

- 초기 언론사: [신화사, 인민일보, 환구시보] ⇒3개
- 확장된 언론사:  [신화사, 인민일보, 환구시보, 해방군보, 경제일보, 광명일보] ⇒6개

![스크린샷 2025-02-19 오전 1.13.37.png](%E1%84%80%E1%85%AE%E1%86%A8%E1%84%8C%E1%85%A6%E1%84%80%E1%85%AA%E1%86%AB%E1%84%80%E1%85%A8%20%E1%84%87%E1%85%AE%E1%86%AB%E1%84%89%E1%85%A5%E1%86%A8%20%E1%84%80%E1%85%AA%E1%84%8C%E1%85%A5%E1%86%BC%201819d1de3e06805f96d7e0d18212ea11/977811f5-8aa2-4924-97ce-5a70a431f177.png)

## Step 2 -Content Crawling

Step 1에서 수집한 URL을 기준으로 기사 본문(text) 가져오기

언론사마다 **HTML 태그 구조가 다르므로** 각각에 맞게 본문을 추출해야 함

**해방군보 경우,** 본문이 HTML 주석(`<!-- -->`) 안에 있어 주석 내 텍스트를 추출하는 기능  필요

```python
# 인민일보의 본문 추출 가능한 HTML
# 다음 태그의 p 태그에 본문이 담겨져 있음
        article_div = (
                soup.find('div', class_='rm_txt_con cf') or
                soup.find('div', id='ozoom') or
                soup.find('div', id='rwb_zw') or
                soup.find('div', id='p_content') or
                soup.find('div', id='content') or
                soup.find('div', class_='content') or
                soup.find('div', class_='article') or
                soup.find('div' , class_='ad_left wb_left fl' ) or
                soup.find('div', class_='text_show') or
                soup.find('div', class_='show_text') or
                soup.find('div', class_='txt clearfix') or
                soup.find('div', class_='content clear clearfix') or
                soup.find('div', class_='txt clearfix') or
                soup.find('font', class_='fbody'))
        if article_div:
            paragraphs = article_div.find_all('p')
            return "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
```

```python

#해방군보의 본문 추출
        article_div = (
                soup.find('div', id='APP-Content') or
                soup.find('div', class_='m-t-list') or
                soup.find('div', id='article-content'))
        extracted_text = []
        
        #isinstance(text, Comment)를 사용하여 HTML <!-- 주석 내용 --> 추출
				if article_div:
				    comments = article_div.find_all(string=lambda text: isinstance(text, Comment))
				    for comment in comments:
				        if comment.strip():  # 빈 주석 제외
				            comment_soup = BeautifulSoup(comment, "html.parser")
				            paragraphs = comment_soup.find_all("p")
				            extracted_text.extend(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))
				
				
				
```

## Step 3 -Keyword Filter

Step 2에서 수집한 기사 본문에서 특정 키워드(한미일 협력 관련 용어)가 포함된 기사만 선별

filtered articles 와 excluded articles로 분리

키워드 개수 증가

- 초기 키워드: ["三边", "三国", "三方"]
- 5개 확장: ["三边", "三国", "三方", "三角", "同盟"]
- 9개 확장: ["三边", "三国", "三方", "三角", "同盟", "3边", "3国", "3方", "3角"]

## Step 4 -Excluded Article Selection

Step 3에서 "삼국 협력 관련 없음"으로 분류된 excluded_articles 중 실제로는 관련된 기사일 가능성이 있는 것들을 **수동 검토하여 추가**

은주 박사님께서 직접 기사 내용을 확인하고 필요한 기사들을 추가

최종적으로 filtered_articles에 포함될 기사들을 업데이트

## Step 5 -Date Crawling

step 1에서 날짜 정보가 없는 기사들의 날짜를 추가로 수집

언론사별로 날짜 추출 방식이 다르므로 맞춤형 크롤링 진행

- 환구시보  → **Selenium을 이용한 동적 크롤링 필요**
- 인민일보 ,경제일보,광명일보 → **URL 도메인에서 날짜 추출 가능**

```python

```

```python

def extract_date_from_URL(url):
    try:
        # /YYYY-MM/DD/ 형식을 추출
        match = re.search(r'/(\d{4}-\d{2})/(\d{2})/', url)
				if match:
				    date = f"{match.group(1)}-{match.group(2)}"  # 예: '2023-08-18
            return date
        else:
            return None  
    except Exception as e:
        print(f"Error extracting date from {url}: {e}")
        return None
        
#/YYYYMM/DD/ 패턴 일 경우 
match = re.search(r'/(\d{6})/(\d{2})/', url)
data = f"{match.group(1)[:4]}-{match.group(1)[4:]}-{match.group(2)}"

#/YYYY-MM/DD/ 패턴 일 경우
match = re.search(r'/(\d{4}-\d{2})/(\d{2})/', url)
date = f"{match.group(1)}-{match.group(2)}"  

```

## Step 6 -Merging Distributed Media Data

Step 5 이후 더 이상 언론사별 개별 작업이 필요 없으므로 모든 데이터를 하나로 병합

## Step 7 -Dudeplication

Step 6에서 병합된 데이터에서 중복 기사  제거

유니크 기사(unique_articles.json)와 중복 기사(duplicate_articles.json) 분리 저장

중복 기사의 2가지 유형

- **(Case 1) 같은 언론사에서 중복된 기사** → URL 또는 제목+본문이 동일한 경우
    - 중복되는 값 중 하나만 남기고 유니크 기사에 추가
    
    ```python
    
    ```
    
- **(Case 2) 여러 언론사에서 동일한 기사** → 제목이 동일하고 본문 유사도가 높음
    - 은주 박사님이 수동으로 선택하여 하나만 유니크 기사에 추가

| 언론사 | 도메인 | raw data 수 | filtered data 수 |  |  |
| --- | --- | --- | --- | --- | --- |
| 신화사 | `xinhuanet.com` | 285개 |  |  |  |
| 인민일보 | `people.com.cn` | 293개 |  |  |  |
| 환구시보 | `globaltimes.cn` | 279개 |  |  |  |
| 해방군보 | [81.cn](http://81.cn/)  | 246개	 |  |  |  |
| 경제일보 | [ce.cn](http://ce.cn/)  | 189개 |  |  |  |
| 광명일보 | [gmw.cn](http://gmw.cn/)  | 154개 |  |  |  |
| 총 |  | 1455개 |  |  |  |
