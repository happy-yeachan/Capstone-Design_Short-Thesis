from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from video_generator.TTS import tts
from video_generator.video_main import merge_videos_with_duration
from video_generator.video_pixabay import pixabay
from video_generator.video_caption import add_automatic_subtitles

import os

app = FastAPI()


# CORS 설정: 모든 출처에서 접근 가능하도록 설정 (필요에 따라 도메인 제한 가능)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 특정 도메인만 허용하려면 "*" 대신 도메인 입력
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/test")
async def root(text: str, tag: str):
    tts(text)
    paths = pixabay(text, tag)
    merge_videos_with_duration(paths)
    add_automatic_subtitles(text, tag)

    return {"message": "Hello World"}


@app.get("/video/{category}/{filename}", response_class=FileResponse)
async def serve_video(category: str, filename: str):
    UPLOAD_DIRECTORY = f"result/{category}"
    file_path = os.path.join(UPLOAD_DIRECTORY, filename)  # 파일 경로 생성

    if os.path.exists(file_path):
        return FileResponse(file_path)  # 파일을 응답으로 반환
    else:
        return {"error": "File not found"}  # 파일이 없을 경우 에러 반환

