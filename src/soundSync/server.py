# waring: do not run this file your self if your don't want
#         to f*ck up your speakers...

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from soundSync.config import settings
from soundSync.utils import initialize_recorder, audio_streaming


@asynccontextmanager
async def lifespan(app: FastAPI):
    # initialize_recorder()
    yield

app = FastAPI(
    docs_url='',
    redoc_url='',
    lifespan=lifespan
)

@app.get("/")
def home():
    return {
          "msg": "Welcome to SoundSync streaming.\n Visit /live for live streaming."
    }

@app.get("/live")
def streaming_audio():
        return StreamingResponse(
            content=audio_streaming(),
            media_type='audio/wav'
        )