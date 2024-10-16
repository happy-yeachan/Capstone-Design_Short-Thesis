from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from video_generator.TTS import tts
from video_generator.video_main import merge_videos_with_duration
from video_generator.video_pixabay import pixabay
from video_generator.video_pexels import pexels_api
from video_generator.video_caption import add_caption
import requests

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 비디오 생성 작업을 비동기로 실행할 함수
async def process_video(text: str, tag: str, id: str):
    tts(text)
    paths = pixabay(text)
    merge_videos_with_duration(paths)
    url = add_caption(text, tag)
    data = {
        "articleId": id,
        "videoUrl": url
    }
    response = requests.post("https://purely-funky-ladybug.ngrok-free.app/save/video", data=data)
    print(response.status_code)
    

# POST 요청 처리 (비디오 제작 요청 및 백그라운드 처리)
@app.post("/movie")
async def create_movie(id: str, text: str, tag: str, background_tasks: BackgroundTasks):
    # 비디오 제작을 백그라운드에서 처리하도록 설정
    background_tasks.add_task(process_video, text, tag, id)

    return {"message": "Video creation in progress", "id": id}

# GET 요청 처리 (비디오 상태 및 파일 반환)
@app.get("/videos/{tag}/{filename}", response_class=FileResponse)
async def serve_video(tag: str, filename: str):
    UPLOAD_DIRECTORY = f"videos/{tag}"
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)  # 파일 경로 생성

    if os.path.exists(file_path):
        return FileResponse(file_path)  # 파일을 응답으로 반환
    else:
        return {"error": "File not found"}  # 파일이 없을 경우 에러 반환

