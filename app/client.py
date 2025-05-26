#Logica do client
import asyncio
import websockets


async def chat():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            message = input("message: ")
            await websocket.send(message)
            response = await websocket.recv()
            print(f"Fibo: {response}")

if __name__ == "__main__":
    asyncio.run(chat())