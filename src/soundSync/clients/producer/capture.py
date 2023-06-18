"""
Create a virtual speaker and stream the sound played 
through that virtual speaker.
"""
from typing import Generator
from functools import partial

import soundfile as sf

# since speaker doesn't work in wsl 
# temporarily streaming a audio recording...

def _generate_blocks(filepath: str, blocksize: int) -> Generator[bytes, None, None]:
    with open(filepath, "rb") as fp:
        block_generator = iter(partial(fp.read, blocksize), b'')

        for block in block_generator:
            yield block


def audio_stream(filepath: str) -> Generator[bytes, None, None]:
    audio_window_size: int = 9
    sample_rate: int = sf.info(filepath).samplerate

    audio_block_size: int = sample_rate * audio_window_size

    audio_generator = _generate_blocks(filepath, audio_block_size)

    return audio_generator

