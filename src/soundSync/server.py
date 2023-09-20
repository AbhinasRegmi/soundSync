# waring: do not run this file your self if your don't want
#         to f*ck up your speakers...

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from soundSync.config import settings
from soundSync.utils import AudioStreamer


streamer = AudioStreamer( 
    n_channels=settings.RECORDING_CHANNEL_NUMBERS,
    sample_rate=settings.RECORDING_SAMPLE_RATE,
    chunk_size=settings.RECORDING_CHUNK_SIZE
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    streamer.start_recording()
    yield
    streamer.stop_recording()

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
            content=streamer.gen_audio(),
            media_type='audio/wav'
        )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)