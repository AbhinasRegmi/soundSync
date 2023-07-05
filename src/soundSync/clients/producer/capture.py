"""
Create a virtual speaker and stream the sound played 
through that virtual speaker.
"""
from typing import Generator
from functools import partial

import soundfile as sf
import sounddevice as sd

from soundSync.config import settings

def start_recording() -> None:
    input_stream = sd.InputStream(
        samplerate=settings.RECORDING_SAMPLE_RATE,
        channels=settings.RECORDING_CHANNEL_NUMBERS
    )

    input_stream.start()

    recording = sd.rec(
        int(5 * settings.RECORDING_SAMPLE_RATE),
        samplerate=settings.RECORDING_SAMPLE_RATE,
        channels=settings.RECORDING_CHANNEL_NUMBERS,
        blocking=True
    )

    input_stream.close()
    

def _generate_blocks(filepath: str, blocksize: int) -> Generator[bytes, None, None]:
    with open(filepath, "rb") as fp:
        block_generator = iter(partial(fp.read, blocksize), b'')

        for block in block_generator:
            yield block


def audio_stream(filepath: str) -> Generator[bytes, None, None]:
    audio_window_size: int = 10
    sample_rate: int = sf.info(filepath).samplerate

    audio_block_size: int = sample_rate * audio_window_size

    audio_generator = _generate_blocks(filepath, audio_block_size)

    return audio_generator

