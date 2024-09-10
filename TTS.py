import urllib.request
from dotenv import load_dotenv
import os

load_dotenv()  # .env 파일에서 환경 변수 불러오기
client_id = os.getenv("NAVER_CLIENT_ID")
client_secret = os.getenv("NAVER_CLIENT_SECRET")


def tts(text):
    encText = urllib.parse.quote(text)
    data = "speaker=nara&volume=0&speed=-2&pitch=0&format=mp3&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    request.add_header("X-NCP-APIGW-API-KEY",client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if(rescode==200):
        print("TTS mp3 저장")
        response_body = response.read()
        with open('test.mp3', 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)

tts("""본 논문에서는 딥 뉴럴 기반의 새로운 모델 없는 접근 방식을 제공합니다
네트워크(DNN)를 통해 포인트 예측 및 예측 간격을 달성합니다
일반적인 회귀 설정. 일반적으로 사람들은 파라메트릭 또는
종속 및 독립 변수(Y 및 X)를 연결하는 비모수적 모델.
그러나 이 고전적인 방법은 올바른 모델에 크게 의존합니다
사양. 비모수적 접근 방식의 경우에도 일부 추가 형식은 다음과 같습니다
종종 가정됩니다. 새로 제안된 모델 없는 예측 원칙은 다음과 같습니다
모델 가정이 없는 예측 절차. 이전 작업에 대한 내용
이 원칙은 다른 표준 대안보다 더 나은 성능을 보여주었습니다.
최근 머신 러닝 방법 중 하나인 DNN이 증가하고 있습니다
실제 성능이 뛰어나 주목을 받고 있습니다. 모델 프리 가이드
예측 아이디어, 우리는 완전 연결 순방향 DNN을 매핑 X에 적용하려고 시도합니다
몇 가지 적절한 참조 무작위 변수 Z ~ Y. 타겟 DNN이 훈련됩니다
특별히 설계된 손실 함수를 최소화하여 Y의 무작위성을 확보합니다
X를 조건으로 하는 것은 훈련된 DNN을 통해 Z로 아웃소싱됩니다. 우리의 방법은 다음과 같습니다
특히 다른 DNN 기반 대응물에 비해 안정적이고 정확합니다
최적의 포인트 예측. 특정 예측 절차를 통해 우리의 예측은
인터벌은 추정 변동성을 포착하여 더 나은 결과를 만들 수 있습니다
유한한 샘플 케이스의 커버리지 비율. 우리 방법의 우수한 성능
는 시뮬레이션 및 경험적 연구를 통해 검증됩니다.""")