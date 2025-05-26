import asyncio

from websockets import ConnectionClosed


async def send(websocket, message):
    try:
        await websocket.send(message)
    except ConnectionClosed:
        pass

def broadcast(message):
    for websocket in CLIENTS:
        asyncio.create_task(send(websocket, message))