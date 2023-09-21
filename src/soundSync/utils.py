import time
import struct
import threading
from typing import Generator
from collections import deque

import pyaudio

class AudioStreamer:
    def __init__(
            self,
            n_channels: int,
            sample_rate: int,
            chunk_size: int
    ) -> None:
        
        self._n_channels = n_channels
        self._sample_rate = sample_rate
        self._chunk_size = chunk_size
        self._thread = threading.Thread(target=self._record_chunks, daemon=True)
        self._buffer: deque[bytes] = deque(maxlen=1)
        self._recorder_stream = self._initialize_recorder()

    def _initialize_recorder(self) -> pyaudio.Stream:
        """
        Initializes the pyaudio recorder and returns a stream.
        Use the stream to start, stop, end recording.
        """

        recorder = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=self._n_channels,
            rate=self._sample_rate,
            input=True,
            frames_per_buffer=self._chunk_size
        )

        return recorder
    
    def _get_wav_header(self) -> bytes:
        """
        Header Format:
        RIFF 0 WAVE
        fmt  16 1 <n_channels> <sample_rate>
        <sample_rate * n_channels * byte_size> <n_channles * byte_size> 16
        data <data_size>
        """

        data_size = 0xFFFFFFFF  #unknown end filesize
        byte_size = 2   #using 16-bits to record so 2 bytes

        HEADER = struct.pack('<4sI4s', b'RIFF', 0, b'WAVE')
        META = struct.pack(
            '<4sIHHIIHH',
            b'fmt ',
            16,
            1,
            self._n_channels,
            self._sample_rate,
            self._sample_rate * self._n_channels * byte_size,
            self._n_channels * byte_size,
            16
        )
        DATABEGIN = struct.pack('<4sI', b'data', data_size)

        return HEADER + META + DATABEGIN

    
    def _record_chunks(self) -> None:
        """
        This will record chunks and submit to the queue.
        Consume the queue to get data from the recording stream.
        Run this on a deamon Thread to automatically close when application closes.
        """

        self._recorder_stream.start_stream()

        while True:
            self._buffer.append(self._recorder_stream.read(self._chunk_size))

    def start_recording(self) -> None:
        """
        Start the deamon thread to start publishing data.
        Data can be accessed through audio method.
        """
        self._thread.start()

    def stop_recording(self) -> None:
        self._recorder_stream.stop_stream()
        self._recorder_stream.close()

    def get_audio(self) -> bytes:
        return self._buffer.popleft()
    
    def gen_audio(self) -> Generator[bytes, None, None]:

        yield self._get_wav_header()

        while True:
            if len(self._buffer) > 0:
                yield self._buffer.popleft()
            else:
                time.sleep(0.001)