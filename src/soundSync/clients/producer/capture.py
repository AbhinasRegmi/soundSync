from typing import Generator

import pyaudio

from soundSync.config import settings

paudio = pyaudio.PyAudio()

#start the stream
stream = paudio.open(
    format=pyaudio.paInt16,
    channels=settings.RECORDING_CHANNEL_NUMBERS,
    rate=settings.RECORDING_SAMPLE_RATE,
    frames_per_buffer=settings.RECORDING_FRAMES_PER_BUFFER,
    input=True
)

# frames = []

# for i in range(0, int(settings.RECORDING_SAMPLE_RATE / settings.RECORDING_FRAMES_PER_BUFFER * 5)):
#     data = stream.read(settings.RECORDING_FRAMES_PER_BUFFER)
#     frames.append(data)

# stream.stop_stream()
# stream.close()

# paudio.terminate()



def audio_stream() -> Generator[bytes, None, None]:
    print("Recording Started...")
    
    while True:
        try:
            data = stream.read(settings.RECORDING_FRAMES_PER_BUFFER)
            yield data
        except:
            print("Recording stopped...")

