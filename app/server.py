#Logica do server
import asyncio
import websockets
from websockets import ConnectionClosed

cl = set()

async def handle_client (websocket, path):
    cl.add(websocket)
    try:
        async for message in websocket:
            for client in cl:
                if client != websocket:
                    await client.send(message)
    except ConnectionClosed:
        pass
    finally:
        cl.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, 'localhost', 8765)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())