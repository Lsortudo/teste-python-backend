#Logica do show_time
import asyncio
import datetime

from websockets import serve
from websockets.legacy.protocol import broadcast


async def show_time(server):
    while True:
        message = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()# .strftime("%d/%m/%Y %H:%M:%S")
        broadcast(server.connection, message)
        await asyncio.sleep(1)
        # message = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # async for message in websocket:
    #    await websocket.send(message)

async def main():
    async with serve(show_time, "localhost", "8000") as server:
        await server.serve_forever()

asyncio.run(main())

# await asyncio.sleep(1)