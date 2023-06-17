"""
Broadcast the data over a certain route.
"""
import asyncio
from soundSync.config import settings

from websockets.server import serve
from websockets.exceptions import ConnectionClosed

CLIENTS = set()

async def request_handler(ws):
    CLIENTS.add(ws)

    try:
        while True:
            data = await ws.recv()

            for client in CLIENTS.copy():
                await client.send(data)
    except ConnectionClosed:
        CLIENTS.remove(ws)


async def run_server() -> None:
    async with serve(request_handler, settings.WEB_SOCKET_URL, settings.WEB_SOCKET_PORT):
        await asyncio.Future() # this makes server run forever.


if __name__ == "__main__":
    asyncio.run(run_server())

