from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip
import os

def add_caption(script, tag, id):
    # 비디오 파일 로드
    video_clip = VideoFileClip("asset/video.mp4")
    video_height = video_clip.h  # 비디오 높이 계산

    # 오디오 클립 불러오기
    audio_clip = AudioFileClip("asset/sound.mp3")
    audio_duration = audio_clip.duration

    # 문장 단위로 나눈 텍스트 리스트
    texts = split_text(script)

    # 각 문장 길이에 비례한 자막 클립 길이 계산
    total_text_length = sum(len(text) for text in texts)
    subtitle_durations = [(len(text) / total_text_length) * audio_duration + 0.1 for text in texts]

    # 자막 클립 리스트 생성
    subtitle_clips = []
    current_time = 0  # 자막 시작 시간

    for i, chunk in enumerate(texts):
        # 텍스트를 25자마다 줄바꿈, 줄 수 제한 없이 자막 클립 리스트로 나누기
        wrapped_chunks = wrap_text(chunk, max_length=25)

        for wrapped_chunk in wrapped_chunks:
            subtitle_clip = (TextClip(wrapped_chunk, fontsize=50, color='white', font='pont.ttf', bg_color='black')
                             .set_position(('center', int(0.6 * video_height)))  # 직접 계산된 위치 사용
                             .set_duration(subtitle_durations[i] / len(wrapped_chunks))
                             .set_start(current_time))

            subtitle_clips.append(subtitle_clip)
            current_time += subtitle_durations[i] / len(wrapped_chunks)  # 각 클립 길이만큼 다음 자막 시작 시간 증가

    # 자막과 비디오 합성
    final_video = CompositeVideoClip([video_clip] + subtitle_clips)
    final_video = final_video.set_audio(audio_clip)

    # 저장할 디렉토리 경로
    output_directory = f"videos/{tag}"

    # 디렉토리가 없으면 생성
    os.makedirs(output_directory, exist_ok=True)

    # 최종 비디오 저장 (ex: 5.mp4)
    final_video.write_videofile(f"{output_directory}/{id}.mp4", fps=24)
    
    return f"{output_directory}/{id}.mp4"

# ?, !, . 기준으로 텍스트를 나누는 함수
def split_text(text):
    import re
    # ? ! . 만을 기준으로 텍스트 나누기
    chunks = re.split(r'(?<=[?!\.])\s*', text)
    # 빈 문자열 제거
    chunks = [chunk for chunk in chunks if chunk]
    return chunks

# 텍스트를 25자마다 줄바꿈하고 여러 자막으로 나누는 함수
def wrap_text(text, max_length=30):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        # 현재 줄에 단어를 추가해도 max_length를 초과하지 않으면 추가
        if len(current_line + " " + word) <= max_length:
            current_line += (word + " ")
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    
    # 마지막 줄 추가
    lines.append(current_line.strip())
    
    # 줄 수 제한 없이 자막 클립으로 나누어 반환
    return lines
