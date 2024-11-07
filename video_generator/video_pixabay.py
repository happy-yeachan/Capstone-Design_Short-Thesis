import requests
import os
import random
from dotenv import load_dotenv
import time

load_dotenv()  # .env 파일에서 환경 변수 불러오기
API_KEY = os.getenv("PIXABAY_API_KEY")


def fetch_with_retry(url, max_retries=3, timeout_duration=30):
    """
    주어진 URL로 요청을 보내고, 실패할 경우 최대 max_retries까지 재시도합니다.
    각 재시도 시 타임아웃 시간을 증가시켜, 일시적인 네트워크 문제를 해결할 수 있게 합니다.
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, stream=True, timeout=timeout_duration)
            response.raise_for_status()  # 응답 상태 코드가 200이 아닐 경우 예외 발생
            return response  # 성공 시 응답 반환
        except requests.exceptions.Timeout:
            # 타임아웃 발생 시 재시도
            retries += 1
            print(f"Timeout occurred. Retrying... ({retries}/{max_retries})")
            time.sleep(2)  # 다음 시도 전 2초 대기
            timeout_duration += 10  # 재시도 시 타임아웃 증가
        except requests.exceptions.RequestException as e:
            # 기타 요청 에러가 발생할 경우 루프 종료
            print(f"Request error: {e}")
            break
    return None  # 모든 시도가 실패할 경우 None 반환

def download_video(video_url, filename, max_retries=3, initial_timeout_duration=30):
    """
    주어진 비디오 URL을 다운로드하고, 최대 max_retries까지 재시도합니다.
    각 재시도 시 타임아웃 시간이 증가하여 안정적인 다운로드가 가능하도록 합니다.
    """
    retries = 0
    timeout_duration = initial_timeout_duration
    while retries < max_retries:
        try:
            # 비디오 파일을 가져오는 fetch_with_retry 호출
            response = fetch_with_retry(video_url, max_retries=1, timeout_duration=timeout_duration)
            if response is None:
                raise requests.exceptions.RequestException("Failed to fetch video after retries.")
            
            # 비디오 파일을 청크 단위로 다운로드하여 로컬 파일에 저장
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Video {filename} downloaded successfully.")
            return True  # 성공적으로 다운로드한 경우 True 반환
        except requests.exceptions.Timeout:
            # 타임아웃 발생 시 재시도
            retries += 1
            timeout_duration += 20  # 재시도 시 타임아웃 증가
            print(f"Timeout on download. Retrying... ({retries}/{max_retries}), Timeout: {timeout_duration}")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            # 기타 요청 에러가 발생할 경우 루프 종료
            print(f"Download error: {e}")
            break
    return False  # 모든 시도가 실패할 경우 False 반환

def pixabay(querys, category):
    """
    주어진 키워드 목록(querys)과 카테고리를 사용하여 Pixabay에서 비디오를 검색하고,
    각 키워드당 2개의 중복되지 않은 비디오를 랜덤하게 선택하여 다운로드합니다.
    """
    i = 1  # 저장 파일의 인덱스 관리
    paths = []  # 다운로드된 비디오 파일 경로를 저장할 리스트

    for query in querys:
        # 키워드와 카테고리를 사용해 Pixabay API 요청 URL 생성
        url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko&category={category}'
        response = fetch_with_retry(url)
        
        # 첫 번째 요청 실패 시 다음 키워드로 넘어감
        if response is None:
            print(f"{query} 키워드로 API 요청이 실패했습니다.")
            continue

        # API 응답을 JSON 형식으로 변환
        data = response.json()
        
        # 결과가 2개 미만인 경우, 카테고리 없이 다시 시도
        if 'hits' in data and len(data['hits']) < 2:
            url = f'https://pixabay.com/api/videos/?key={API_KEY}&q={query}&lang=ko'
            response = fetch_with_retry(url)
            if response is None:
                print(f"재요청 실패. {query} 키워드에 대한 영상을 찾을 수 없습니다.")
                continue
            data = response.json()

        # 여전히 결과가 2개 미만이면 다음 키워드로 넘어감
        if 'hits' in data and len(data['hits']) < 2:
            print(f"Pixabay에서 {query} 키워드에 대한 충분한 영상을 찾을 수 없습니다.")
            continue

        # 중복 없이 두 개의 영상을 랜덤 선택
        videos = random.sample(data['hits'], 2)
        print(f"비디오 키워드: {query}")

        for video in videos:
            # 선택한 비디오의 URL 가져오기
            video_url = video['videos']['medium']['url']
            video_filename = f'asset/video_{i}.mp4'
            
            # 비디오 다운로드, 성공 시 경로 저장 및 인덱스 증가
            if download_video(video_url, video_filename):
                paths.append(video_filename)
                i += 1
            else:
                print(f"비디오 다운로드 실패: {video_url}")

            time.sleep(1)  # API 호출 간 1초 대기

    return paths  # 모든 다운로드된 비디오 파일 경로 반환