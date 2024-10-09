from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os
import shutil


def get_next_video_number(directory):
    # 디렉토리 내 파일 목록을 가져오기
    files = os.listdir(directory)
    
    # 숫자로 끝나는 .mp4 파일 필터링 및 숫자 추출
    numbers = []
    for file in files:
        if file.endswith(".mp4"):
            try:
                # 파일 이름에서 숫자 부분만 추출 (예: 5.mp4 -> 5)
                num = int(file.split(".")[0])
                numbers.append(num)
            except ValueError:
                continue  # 숫자가 아닌 경우 무시
    
    if numbers:
        return max(numbers) + 1  # 가장 큰 숫자에 1을 더해 반환
    else:
        return 1  # 파일이 없으면 1부터 시작

def add_caption(script, tag):
    # 비디오 파일 로드
    video_clip = VideoFileClip("asset/video.mp4")
    video_height = video_clip.h  # 비디오 높이 계산

    # 오디오 클립 불러오기
    audio_clip = AudioFileClip("asset/sound.mp3")
    audio_duration = audio_clip.duration

    # 나눈 텍스트 리스트
    texts = split_text(script)

    # 텍스트에 대한 클립 길이 계산
    text_duration = audio_duration / len(texts) + 0.1

    # 대본을 일정 글자 수로 나누기
    chunks = split_text(script)

    # 자막 클립 리스트 생성
    subtitle_clips = []
    current_time = 0  # 자막 시작 시간

    for chunk in chunks:
        subtitle_clip = (TextClip(chunk, fontsize=50, color='white', font='pont.ttf', bg_color='black')
                         .set_position(('center', int(0.6 * video_height)))  # 직접 계산된 위치 사용
                         .set_duration(text_duration)
                         .set_start(current_time))

        subtitle_clips.append(subtitle_clip)
        current_time += text_duration  # 다음 자막 시작 시간 계산

    # 자막과 비디오 합성
    final_video = CompositeVideoClip([video_clip] + subtitle_clips)
    final_video = final_video.set_audio(audio_clip)

    # 저장할 디렉토리 경로
    output_directory = f"videos/{tag}"

    # 디렉토리가 없으면 생성
    os.makedirs(output_directory, exist_ok=True)

    # 저장할 파일의 다음 번호 가져오기
    next_number = get_next_video_number(output_directory)

    # 최종 비디오 저장 (ex: 5.mp4)
    final_video.write_videofile(f"{output_directory}/{next_number}.mp4", fps=24)
    
    return f"{output_directory}/{next_number}.mp4"

# 글자 수에 맞춰 비슷한 길이로 나누는 함수
def split_text(text, chunk_size=25):  # chunk_size 조정 가능
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


# # 예시 사용
# script = "안녕하세요! 요즘 쇼핑, 그냥 물건 사는 것만으로 끝나지 않죠? 쇼핑이 하나의 즐거운 경험으로 변하고 있어요. 그래서 오늘은 이런 변화를 반영한 새로운 쇼핑센터에 대해 이야기해 볼게요. 우리 연구는 일본의 4곳의 쇼핑센터를 조사했어요. 그 결과, 이곳들은 곡선형 통로를 갖고 있어서 사람들이 끊임없이 움직이는 모습을 볼 수 있어요. 그리고 각 구역마다 독특한 테마가 있어서 걷는 동안 다양한 스토리를 체험할 수 있답니다. 리테일 샵, 레스토랑, 문화 공간도 각각의 영역이 잘 구분되어 있어서 더 흥미로워요. 이렇게 쇼핑센터가 하나의 테마파크처럼 변하고 있는 거죠. 여러분도 이런 곳에서 쇼핑해보고 싶지 않나요? 이처럼 쇼핑은 이제 단순한 소비가 아니라, 다양한 경험과 스토리를 제공하는 멋진 활동이 되었어요. 앞으로 더 많은 쇼핑센터가 이런 트렌드를 따라가게 될 거예요. 기대되지 않나요?"
# add_automatic_subtitles(script)
