"""
Receive data from a single client.
"""

from websockets.server import serve


async def receive_data(ws):
    async for data in ws:
        ...