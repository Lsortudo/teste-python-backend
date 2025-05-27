import asyncio
import json

import websockets
from datetime import datetime

from fibonacci import fibonacci


async def handle_comms(websocket):
    async def send_timer(ws):
        try:
            while True:
                now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                await ws.send(now)
                await asyncio.sleep(1)
        #except websockets.exceptions.ConnectionClosed:
        except websockets.ConnectionClosed:
            print("Cliente desconectado")

    async def send_question(ws):
        try:
            async for message in ws:
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
            return

    comms_task = asyncio.create_task(send_timer(websocket))
    question_task = asyncio.create_task(send_question(websocket))

    result1 = await comms_task
    result2 = await question_task

async def main():
    async with websockets.serve(handle_comms, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
