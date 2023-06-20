"""
A pc client that listens to webserver
"""
import base64
from soundSync.config import settings

from websockets.client import connect
from websockets.exceptions import ConnectionClosed


async def listen() -> None:
    async with connect(settings.WEB_SOCKET_FULL_URL) as ws:
        try:
            with open("./temp.mp4", 'wb') as fp:
                while True:
                    data = await ws.recv()

                    binary_data = base64.b64decode(data)
                    if not isinstance(binary_data, bytes):
                        raise ValueError("Data received must be bytes.")

                    fp.write(binary_data)
        except ConnectionClosed:
            print(f"Error: Server Disconnected ...")


if __name__ == "__main__":
    import asyncio

    asyncio.run(listen())