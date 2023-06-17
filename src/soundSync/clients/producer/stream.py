"""
Upload the audio stream to websocket for broadcasting.
"""

from websockets.client import connect

from soundSync.config import settings
from soundSync.clients.producer.capture import audio_stream

path = "/home/abhinas/Development/Python/soundSync/audio/mooskan.MP3"


async def upload() -> None:
    """
    Consumes the audio_stream generattor and uploads to 
    certain websocket.
    """

    # this is temporary
    stream = audio_stream(path)

    
    async with connect(settings.WEB_SOCKET_FULL_URL) as ws:
        for packet in stream:
            await ws.send(packet)



if __name__ == "__main__":
    import asyncio

    asyncio.run(upload())