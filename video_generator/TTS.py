import urllib.request
from dotenv import load_dotenv
import os
import random  # 랜덤 선택을 위해 random 모듈 추가

load_dotenv()  # .env 파일에서 환경 변수 불러오기
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")

# speaker 리스트
speaker = ["vara", "vmikyung", "vdain", "vyuna", "vhyeri", "vian", "vdonghyun", "vgoeun", "vdaeseong", "nmovie"]

def tts(text):
    encText = urllib.parse.quote(text)
    
    # speaker 리스트에서 랜덤으로 하나 선택
    random_speaker = random.choice(speaker)
    
    # 선택된 speaker 값을 사용하여 data 문자열 완성
    data = f"speaker={random_speaker}&volume=0&speed=-2&pitch=0&format=mp3&text=" + encText
    
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    
    if rescode == 200:
        print("TTS mp3 저장")
        response_body = response.read()
        with open('asset/sound.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:", rescode)


# tts("""오늘은 컴퓨터 기술이 어떻게 발전해왔고, 앞으로 어떻게 발전할지 예측하는 방법을 알려주는 논문을 소개할게요! 지금까지 많은 연구들이 유행이나 핫이슈에 맞춰 주제를 정해왔대요. 그런데 이렇게 하면 깊이 있는 결과를 얻기 어렵다고 해요. 그래서 이 논문에서는 컴퓨터 기술을 연구할 때 기술의 큰 흐름을 따라가야 한다고 말하고 있어요. 그중에서도 프로그래밍 언어가 어떻게 발전해왔는지를 살펴보고, 그 흐름을 따라 미래를 예측하는 방법을 제안하고 있어요. 쉽게 말해, 과거의 기술 변화를 잘 이해하면, 미래의 기술이 어떻게 발전할지 미리 준비할 수 있다는 거예요! 컴퓨터와 프로그래밍에 관심 있는 친구들, 꼭 한 번 읽어보면 좋을 것 같아요!""")