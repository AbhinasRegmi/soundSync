import struct
from typing import Generator
from functools import lru_cache
from contextlib import contextmanager

import sounddevice as sd

from soundSync.config import settings


def get_wav_headers(
        n_channels: int,
        sample_rate: int,
        byte_size: int,
        data_size: int
) -> bytes:
    """
    data_size(in_bytes) of -1 represents unknown file size.
    byte_size means how many bytes used. Like 2 if 16-bit audio used.

    Header Format:
        RIFF 0 WAVE
        fmt  16 1 <n_channels> <sample_rate>
        <sample_rate * n_channels * byte_size> <n_channles * byte_size> 16
        data <data_size>
    """
    if data_size < -1:
        raise ValueError("Data Size Cannot be less than -1")
    
    if data_size == -1:
        data_size = 0xFFFFFFFF #this means unkown size
    
    HEADER = struct.pack('<4sI4s', b'RIFF', 0, b'WAVE')
    META = struct.pack(
        '<4sIHHIIHH',
        b'fmt ',
        16,
        1,
        n_channels,
        sample_rate,
        sample_rate * n_channels * byte_size,
        n_channels * byte_size,
        16
    )
    DATABEGIN = struct.pack('<4sI', b'data', data_size)

    return HEADER + META + DATABEGIN



def __gen_audio(
        n_channels: int = 2,
        sample_rate: int = 44100,
        chunk_size: int = 16) -> Generator[bytes, None, None]:
    
    
    
    stream = sd.rec(frames=chunk_size, samplerate=sample_rate, n_channels=2)

    while True:
        yield stream.wait()


gen_wav_audio = __gen_audio()


def audio_streaming() -> Generator[bytes, None, None]:
    try:
        yield(
            get_wav_headers(
                n_channels=settings.RECORDING_CHANNEL_NUMBERS,
                sample_rate=settings.RECORDING_SAMPLE_RATE,
                byte_size=2,
                data_size=-1
            )
        )
        
        yield from __gen_audio(
            n_channels=settings.RECORDING_CHANNEL_NUMBERS,
            sample_rate=settings.RECORDING_SAMPLE_RATE
        )

    finally:
        # stream = initialize_recorder()
        # stream.stop_stream()
        pass
