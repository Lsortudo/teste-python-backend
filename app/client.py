#Logica do client
import asyncio
import json
import websockets

async def chat():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            message = input("Digite um NÚMERO: ")
            await websocket.send(message)
            response = await websocket.recv()
            data = json.loads(response)

            if data["type"] == "fibo":
                print(f"Fibonacci({data['input']}) = {data['result']}")
            elif data["type"] == "error":
                print(f"Erro: {data['message']}")

if __name__ == "__main__":
    asyncio.run(chat())
