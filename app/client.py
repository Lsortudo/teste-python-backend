import asyncio
import json
import uuid

import websockets
import os

async def authenticate(ws,user_id):
    try:
      message = json.dumps({"type": "auth", "data": user_id})
      await ws.send(message)
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor encerrada.")

async def receive_messages(ws):
    try:
        while True:
            message = await ws.recv()
            try:
                data = json.loads(message)
                if data["type"] == "fibo":
                    print(f"\n\nFibonacci de {data['input']}: {data['data']}\n\n")
                elif data["type"] == "error":
                    print(f"Erro: {data['message']}")
                elif data["type"] == "time":
                    print(f"Horário atual: {data['data']}")
            except json.JSONDecodeError:
                print(f"Ocorreu um erro de json decode")
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor encerrada.")

async def send_input_from_usr(ws):
    try:
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Digite um número para calcular o Fibonacci:\n")
            try:
                n = int(user_input)
            except ValueError:
                print("Invalid")
                continue
            user_input_json = json.dumps({"type": "fibo", "data": n})
            await ws.send(user_input_json)
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor encerrada.")

async def main():
    user_id = os.environ["USER"]
    connection = os.environ["WS"]
    skip_user_input = os.environ["SKIP_USER_INPUT"]

    if user_id == "":
        user_id = "default"
    if connection == "":
        connection = "ws://localhost:2222"
    async with websockets.connect(connection) as websocket:
        print("Conectado ao servidor.")
        await authenticate(websocket, user_id)

        tasks = []
        if skip_user_input != "true":
            tasks.append(send_input_from_usr(websocket))

        tasks.append(receive_messages(websocket))

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
