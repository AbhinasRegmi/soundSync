"""
Upload the audio stream to websocket for broadcasting.
"""

import asyncio
from websockets.client import connect

from soundSync.clients.config import settings
from soundSync.clients.pc.capture import audio_stream


async def upload() -> None:
    """
    Consumes the audio_stream generattor and uploads to 
    certain websocket.
    """

    # this is temporary
    stream = audio_stream("./audio/mooskan.MP3")

    
    async with connect(settings.WEB_SOCKET_STREAMING_URL) as ws:
        for packet in stream:
            await ws.send(packet.tobytes())

