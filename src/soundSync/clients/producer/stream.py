"""
Upload the audio stream to websocket for broadcasting.
"""
import base64
from websockets.client import connect

from soundSync.config import settings
from soundSync.clients.producer.capture import audio_stream


async def upload() -> None:
    """
    Consumes the audio_stream generattor and uploads to 
    certain websocket.
    """
    stream = audio_stream()

    
    async with connect(settings.WEB_SOCKET_FULL_URL) as ws:
        for chunk in stream:
            encoded_payload = base64.b64encode(chunk).decode('utf-8')
            await ws.send(encoded_payload)


if __name__ == "__main__":
    import asyncio

    asyncio.run(upload())