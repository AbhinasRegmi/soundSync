from functools import lru_cache
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    WEB_SOCKET_STREAMING_URL: str = "wss://upload"


@lru_cache(maxsize=1)
def setting() -> Config:
    return Config()

settings = setting()