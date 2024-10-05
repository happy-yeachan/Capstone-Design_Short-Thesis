import requests
import os
import random
from dotenv import load_dotenv
from video_generator.keyword_extraction import extract_keywords

load_dotenv()  # .env 파일에서 환경 변수 불러오기
API_KEY = os.getenv("PIXABAY_API_KEY")

# 카테고리와 해당 키워드 정의 (한국어)
categories_keywords = {
    'backgrounds': ['배경', '풍경', '전경', '장면', '스케치', '배경화면', '경관', '배경지식'],
    'fashion': ['패션', '의류', '스타일', '트렌드', '모델', '디자인', '옷', '액세서리', '유행'],
    'nature': ['자연', '야생', '숲', '산', '바다', '강', '호수', '환경', '지구', '식물', '동물', '기후'],
    'science': ['실험', '과학', '연구', '학습', '화학', '물리학', '생물학', '이론', '과학적', '데이터'],
    'education': ['학교', '학습', '교육', '교실', '학생', '선생님', '강의', '수업', '학위', '커리큘럼'],
    'feelings': ['감정', '느낌', '사랑', '행복', '슬픔', '두려움', '기쁨', '정서', '우울', '희망'],
    'health': ['건강', '의학', '운동', '영양', '식이요법', '정신건강', '피트니스', '건강검진', '약물'],
    'people': ['사람', '커뮤니티', '인간', '인물', '사회', '문화', '관계', '인종', '집단'],
    'religion': ['종교', '신앙', '믿음', '교회', '기도', '신', '성경', '불교', '종교적', '영성'],
    'places': ['장소', '도시', '위치', '국가', '지역', '관광지', '명소', '행사', '건축물'],
    'animals': ['동물', '개', '고양이', '야생동물', '서식지', '종', '보호', '애완동물', '생물', '야생'],
    'industry': ['산업', '제조', '생산', '공장', '경제', '노동', '기술', '인프라', '업종', '기업'],
    'computer': ['컴퓨터', '기술', '소프트웨어', '하드웨어', '프로그래밍', '데이터베이스', 'AI', 'IT', '네트워크'],
    'food': ['음식', '요리', '식당', '식사', '레시피', '간식', '건강식', '디저트', '맛집', '식문화'],
    'sports': ['스포츠', '경기', '대회', '팀', '운동', '선수', '훈련', '레크리에이션', '종목', '챔피언'],
    'transportation': ['교통', '차', '기차', '비행기', '버스', '교통수단', '도로', '항공', '운송'],
    'travel': ['여행', '여행지', '휴가', '관광', '탐험', '관광지', '여행사', '일정', '경험'],
    'buildings': ['건물', '건축', '건설', '디자인', '구조물', '주택', '아파트', '사무실', '인프라'],
    'business': ['비즈니스', '재무', '회사', '기업', '상업', '거래', '마케팅', '회계', '전략'],
    'music': ['음악', '노래', '악기', '멜로디', '리듬', '콘서트', '장르', '작곡', '연주']
}

def categorize_script(script):
    # 대본을 소문자로 변환 후 각 단어를 분리
    script_words = script.split()  # 한국어에서는 공백으로 단어 분리

    # 각 카테고리별로 카운트
    category_count = {category: 0 for category in categories_keywords}

    for word in script_words:
        for category, keywords in categories_keywords.items():
            if word in keywords:
                category_count[category] += 1

    # 가장 많은 키워드가 속한 카테고리를 반환
    best_category = max(category_count, key=category_count.get)

    return best_category

def pixabay(text):
    # 검색할 키워드와 요청 URL 설정 (비디오 검색)
    querys = extract_keywords(text)
    category = categorize_script(text)

    i = 1

    paths = []
    for query in querys:

        url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko&category={category}'  # 언어 파라미터 추가
        # API 호출
        response = requests.get(url)
        data = response.json()

        if 'hits' in data and len(data['hits']) <= 0:
            url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko'
            response = requests.get(url)
            data = response.json()

        random_video = random.choice(data['hits'])  # 랜덤으로 하나 선택
        video_url = random_video['videos']['medium']['url']
        print(f"비디오 키워드: {query}")

        # 비디오 다운로드 및 크기 조정
        video_response = requests.get(video_url, stream=True)

        # 저장할 비디오 파일 경로
        video_filename = f'asset/video_{i}.mp4'
        with open(video_filename, 'wb') as f:
            f.write(video_response.content)
        print('비디오가 성공적으로 저장되었습니다.')
        i += 1
        paths.append(video_filename)

    return paths
