import requests
import os
import random
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 불러오기
API_KEY = os.getenv("PIXABAY_API_KEY")

# 검색할 키워드와 요청 URL 설정 (비디오 검색)
query = '컴퓨터'  # 원하는 검색어
url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko'  # 언어 파라미터 추가

# API 호출
response = requests.get(url)
data = response.json()

# 결과에서 랜덤 비디오 URL 가져오기
if 'hits' in data and len(data['hits']) > 0:
    random_video = random.choice(data['hits'])  # 랜덤으로 하나 선택
    video_url = random_video['videos']['medium']['url']
    print(f"랜덤 비디오 URL: {video_url}")

    # 비디오 다운로드
    video_response = requests.get(video_url)

    # 비디오 저장
    with open('downloaded_video.mp4', 'wb') as f:
        f.write(video_response.content)
    print('비디오가 성공적으로 저장되었습니다.')
else:
    print('비디오를 찾을 수 없습니다.')
