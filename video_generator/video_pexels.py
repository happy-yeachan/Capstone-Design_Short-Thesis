import requests
import random
from dotenv import load_dotenv
import os
from googletrans import Translator
from video_generator.keyword_extraction import extract_keywords

# 번역기 객체 생성
translator = Translator()

# 환경 변수에서 API 키 불러오기
load_dotenv()  
API_KEY = os.getenv("PEXELS_API_KEY")

# 요청할 URL
url = 'https://api.pexels.com/videos/search'

# 헤더에 API 키 추가
headers = {
    'Authorization': API_KEY
}

def pexels_api(text):
    # 키워드 추출
    querys = extract_keywords(text)
    print(f"추출된 키워드: {querys}")

    i = 1  # 저장 파일의 인덱스 관리
    paths = []  # 저장된 비디오 경로 리스트

    for query in querys:
        try:
            # 한글 키워드를 영어로 번역
            translated_query = translator.translate(query, src='ko', dest='en').text
            print(f"번역된 키워드: {translated_query}")

            # 검색 파라미터 설정
            params = {
                'query': translated_query,  # 검색할 키워드
                'per_page': 50,             # 한 페이지에 가져올 결과 수
                'page': 1                   # 페이지 번호
            }

            # GET 요청 보내기
            response = requests.get(url, headers=headers, params=params)

            # 응답 결과 처리
            if response.status_code == 200:
                data = response.json()
                videos = data.get('videos', [])

                if videos:
                    # 랜덤한 비디오 선택
                    random_video = random.choice(videos)

                    # 비디오 파일 중 HD 파일 우선 선택
                    video_files = random_video.get('video_files', [])
                    hd_file = next((file for file in video_files if file['quality'] == 'hd'), None)
                    selected_file = hd_file if hd_file else video_files[0] if video_files else None

                    if selected_file:
                        # 비디오 파일 다운로드
                        video_url = selected_file['link']
                        video_content = requests.get(video_url).content

                        # 저장할 비디오 파일 경로 설정
                        video_filename = f'asset/video_{i}.mp4'
                        os.makedirs('asset', exist_ok=True)  # 폴더가 없다면 생성

                        with open(video_filename, 'wb') as video_file:
                            video_file.write(video_content)

                        print(f'비디오 "{translated_query}" 키워드로 성공적으로 저장되었습니다: {video_filename}')
                        paths.append(video_filename)
                        i += 1
                    else:
                        print(f"{translated_query} 키워드에 대한 비디오 파일을 찾을 수 없습니다.")
                else:
                    print(f"{translated_query} 키워드에 대한 비디오를 찾을 수 없습니다.")
            else:
                print(f"Pexels API 요청 실패 (HTTP {response.status_code}): {response.text}")

        except Exception as e:
            print(f"오류 발생: {e}")

    return paths
