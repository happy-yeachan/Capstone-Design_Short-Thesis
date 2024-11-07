import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def merge_videos_with_duration(video_paths, output_size=(1080, 1920)):
    # 오디오 클립 불러오기
    audio_clip = AudioFileClip("asset/sound.mp3")
    total_duration = audio_clip.duration

    # 각 비디오를 로드하고 길이 정보를 가져옴
    original_durations = []
    clips = []
    
    for video in video_paths:
        # 파일 경로에 특수 문자가 없는지 확인
        if not os.path.exists(video):
            print(f"파일이 존재하지 않음: {video}")
            continue
        
        try:
            clip = VideoFileClip(video)
            original_durations.append(clip.duration)
            clips.append(clip)
        except UnicodeDecodeError as e:
            print(f"파일 디코딩 중 오류 발생: {e}")
            continue
    
    if not clips:
        print("처리할 비디오가 없습니다.")
        return

    total_original_duration = sum(original_durations)

    # 각 비디오의 비율에 따라 새로운 길이 설정
    new_durations = [(duration / total_original_duration) * total_duration for duration in original_durations]

    resized_clips = []
    for clip, new_duration in zip(clips, new_durations):
        # 비디오 클립 길이 조정 및 크기 조정
        resized_clip = clip.set_duration(new_duration).resize(output_size)
        resized_clips.append(resized_clip)

    # 모든 비디오 클립을 이어붙임
    final_clip = concatenate_videoclips(resized_clips)
    final_clip = final_clip.set_audio(audio_clip)  # 오디오 추가
    final_clip.write_videofile("asset/video.mp4", fps=24)

    # 최종 처리 후 메모리 해제
    for clip in clips:
        clip.close()
    final_clip.close()
    audio_clip.close()