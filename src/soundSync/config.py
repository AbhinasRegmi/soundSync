from functools import lru_cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    WEB_SOCKET_PORT: int = 8000
    WEB_SOCKET_URL: str = "localhost"
    WEB_SOCKET_FULL_URL: str = f"ws://localhost:8000"

    WEB_HTTP_PORT: int = 5000
    WEB_HTTP_URL: str = "localhost"
    WEB_HTTP_FULL_URL: str = f"localhost:5000"

    RECORDING_SAMPLE_RATE: int = 44100
    RECORDING_CHANNEL_NUMBERS: int = 2
    RECORDING_FRAMES_PER_BUFFER: int = 1024 * 5


@lru_cache(maxsize=1)
def setting() -> Config:
    return Config()

settings = setting()