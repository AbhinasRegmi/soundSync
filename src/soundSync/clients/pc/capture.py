"""
Create a virtual speaker and stream the sound played 
through that virtual speaker.
"""
from typing import Generator

import numpy.typing as np
from numpy import float64
import soundfile as sf

# since speaker doesn't work in wsl 
# temporarily streaming a audio recording...

def audio_stream(filepath: str) -> Generator[np.NDArray[float64], None, None]:
    audio_window_size: int = 10
    sample_rate: int = sf.info(filepath).samplerate

    audio_block_size: int = sample_rate * audio_window_size

    audio_generator = sf.blocks(filepath, blocksize=audio_block_size)

    return audio_generator

