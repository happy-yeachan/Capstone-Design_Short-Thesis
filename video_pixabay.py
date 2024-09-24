import requests
import os
import random
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from keyword_extraction import extract_keywords

load_dotenv()  # .env 파일에서 환경 변수 불러오기
API_KEY = os.getenv("PIXABAY_API_KEY")


def pixabay(text, tag):
    # 검색할 키워드와 요청 URL 설정 (비디오 검색)
    querys = extract_keywords(text)

    i = 1

    paths = []
    for query in querys:
        url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko&category={tag}'  # 언어 파라미터 추가

        # API 호출
        response = requests.get(url)
        data = response.json()

        # 결과에서 랜덤 비디오 URL 가져오기
        if 'hits' in data and len(data['hits']) > 0:
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

        else:
            print(f'{query} 비디오를 찾을 수 없습니다.')

    return paths
