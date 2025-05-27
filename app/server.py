#Logica do server
import asyncio
import json
import websockets
from fibonacci import fibonacci

async def handle_client(websocket):
    try:
        async for message in websocket:
            print(f"Recebido: {message}")
            try:
                n = int(message.strip())
                result = fibonacci(n)
                response = json.dumps({"type": "fibo", "input": n, "result": result})
                await websocket.send(response)
            except ValueError:
                await websocket.send(json.dumps({
                    "type": "error", "message": "Digite um número válido."
                }))
    except websockets.ConnectionClosed:
        print("Cliente desconectado")

async def main():
    async with websockets.serve(handle_client, "localhost", 8765):
        print("Servidor iniciado em ws://localhost:8765")
        while True:
            await asyncio.sleep(1)
        # await asyncio.Future()  # talvez tenha jeito melhor mas esse aqui mantem rodando tbm

if __name__ == "__main__":
    asyncio.run(main())
