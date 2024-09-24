from fastapi import FastAPI
from video_generator.TTS import tts
from video_generator.video_main import merge_videos_with_duration
from video_generator.video_pixabay import pixabay
from video_generator.video_caption import add_automatic_subtitles
app = FastAPI()


@app.post("/test")
async def root(text: str, tag: str):
    tts(text)
    paths = pixabay(text, tag)
    merge_videos_with_duration(paths)
    add_automatic_subtitles(text)

    return {"message": "Hello World"}