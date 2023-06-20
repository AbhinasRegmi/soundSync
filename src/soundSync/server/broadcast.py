"""
Broadcast the data over a certain route.
"""

import asyncio
from collections import deque
from soundSync.config import settings

from websockets.server import serve
from websockets.exceptions import ConnectionClosed

CLIENTS = set()
AUDIO_QUEUE = deque()


async def send_message():
    try:
        while True:
            if AUDIO_QUEUE:
                data = AUDIO_QUEUE.popleft()

                for ws in CLIENTS.copy():
                    try:
                        await ws.send(data)
                    except ConnectionClosed:
                        CLIENTS.remove(ws)
                    except KeyError:
                        pass
            else:
                await asyncio.sleep(0.6)
    except ConnectionClosed:
        pass


async def request_handler(ws):
    CLIENTS.add(ws)

    try:
        while True:
            audio_data = await ws.recv()
            AUDIO_QUEUE.append(audio_data)
    except ConnectionClosed:
        pass


async def run_server() -> None:
    async with serve(request_handler, settings.WEB_SOCKET_URL, settings.WEB_SOCKET_PORT):
        print(f"Started server at {settings.WEB_SOCKET_FULL_URL}")

        asyncio.create_task(send_message())
        await asyncio.Future() # this makes server run forever.


if __name__ == "__main__":
    asyncio.run(run_server())

