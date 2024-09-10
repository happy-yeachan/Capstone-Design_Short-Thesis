import requests
import xml.etree.ElementTree as ET

# arXiv API 엔드포인트
api_url = "http://export.arxiv.org/api/query"

# 검색할 쿼리와 파라미터 설정
params = {
    "search_query": "all:Deep fake",
    "start": 0,
    "max_results": 5,
    "sortBy": "lastUpdatedDate",  # 최신 논문 정렬
    "sortOrder": "descending",    # 최신순 정렬
}


# API 요청
response = requests.get(api_url, params=params)

# 응답 상태 확인
if response.status_code == 200:
    # 응답 데이터(XML)를 파싱
    root = ET.fromstring(response.content)
    
    # 각 논문(entry) 정보를 파싱
    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        summary = entry.find("{http://www.w3.org/2005/Atom}summary").text
        published = entry.find("{http://www.w3.org/2005/Atom}published").text
        link = entry.find("{http://www.w3.org/2005/Atom}id").text
        
        print(f"Title: {title}")
        print(f"Published: {published}")
        print(f"Summary: {summary}")
        print(f"Link: {link}")
        print("-" * 80)
else:
    print(f"Failed to retrieve data: {response.status_code}")