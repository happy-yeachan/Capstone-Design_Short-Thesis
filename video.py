from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

# 주어진 텍스트 내용
full_text = (
    "오늘은 컴퓨터 기술이 어떻게 발전해왔고, 앞으로 어떻게 발전할지 예측하는 방법을 알려주는 논문을 소개할게요! 지금까지 많은 연구들이 유행이나 핫이슈에 맞춰 주제를 정해왔대요. 그런데 이렇게 하면 깊이 있는 결과를 얻기 어렵다고 해요. 그래서 이 논문에서는 컴퓨터 기술을 연구할 때 기술의 큰 흐름을 따라가야 한다고 말하고 있어요. 그중에서도 프로그래밍 언어가 어떻게 발전해왔는지를 살펴보고, 그 흐름을 따라 미래를 예측하는 방법을 제안하고 있어요. 쉽게 말해, 과거의 기술 변화를 잘 이해하면, 미래의 기술이 어떻게 발전할지 미리 준비할 수 있다는 거예요! 컴퓨터와 프로그래밍에 관심 있는 친구들, 꼭 한 번 읽어보면 좋을 것 같아요!"
)

# 글자 수에 맞춰 비슷한 길이로 나누는 함수
def split_text(text, chunk_size=30):  # chunk_size 조정 가능
    chunks = []
    current_chunk = ""
    
    for char in text:
        current_chunk += char
        if len(current_chunk) >= chunk_size:  # 지정된 길이에 도달하면
            chunks.append(current_chunk)
            current_chunk = ""  # 다음 글자부터 새로 시작
            
    if current_chunk:  # 남은 글자 추가
        chunks.append(current_chunk)
        
    return chunks

# 나눈 텍스트 리스트
texts = split_text(full_text)

# 텍스트 이미지를 생성하는 함수
def create_text_image(text, font_path):
    font = ImageFont.truetype(font_path, 40)
    image = Image.new('RGB', (1080, 384), color='black')
    draw = ImageDraw.Draw(image)

    y_position = image.height - 250  # 아래쪽에서 여백을 주고 시작
    text_width = draw.textbbox((0, 0), text, font=font)[2]
    x_position = (image.width - text_width) // 2  # 중앙 정렬

    draw.text((x_position, y_position), text, font=font, fill='white')  # 텍스트 그리기
    return image

# 이미지 클립을 생성할 리스트
image_clips = []
font_path = "pont.ttf"  # 한글 폰트 경로

# 오디오 클립 불러오기
audio_clip = AudioFileClip("test.mp3")
audio_duration = audio_clip.duration

# 텍스트에 대한 클립 길이 계산
text_duration = audio_duration / len(texts)

for text in texts:
    img = create_text_image(text, font_path)
    img.save("temp_image.png")
    clip = ImageClip("temp_image.png").set_duration(text_duration+0.07)
    image_clips.append(clip)

# 모든 이미지 클립을 합치기
final_clip = concatenate_videoclips(image_clips, method="compose")
final_clip = final_clip.set_audio(audio_clip)

# 최종 영상 저장
final_clip.write_videofile("computer_technology_video_short.mp4", fps=24)
