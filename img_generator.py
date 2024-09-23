import requests
from PIL import Image
from io import BytesIO

from PyKakao import Karlo
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일에서 환경 변수 불러오기
client_id = os.getenv("KAKAO_API_KEY")


api = Karlo(service_key = client_id)


# 프롬프트에 사용할 제시어
text = "Computer"

# 이미지 생성하기 REST API 호출
img_dict = api.text_to_image(text, 1)


img_str = img_dict.get("images")[0].get('image')



# URL에서 이미지 데이터를 가져오기
response = requests.get(img_str)

# 이미지 데이터가 제대로 불러와졌는지 확인
if response.status_code == 200:
    # 이미지를 바이너리 데이터로 변환
    img_data = BytesIO(response.content)
    
    # 이미지를 Pillow로 열기
    img = Image.open(img_data)
    
    # 이미지 저장하기
    img.save("./downloaded_image.png")
    print("이미지가 성공적으로 저장되었습니다.")
else:
    print("이미지를 불러오지 못했습니다. 상태 코드:", response.status_code)