from functools import lru_cache
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    RECORDING_SAMPLE_RATE: int = 44100
    RECORDING_CHANNEL_NUMBERS: int = 2
    RECORDING_CHUNK_SIZE: int = 1024
                                
@lru_cache(maxsize=1)
def setting() -> Config:
    return Config()

settings = setting()