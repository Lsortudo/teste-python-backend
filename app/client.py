import asyncio
import json
import uuid

import websockets
import os

async def authenticate(ws,user_id):
    try:
      message = json.dumps({"type": "auth", "data": user_id}) # TODO: get from var
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
                    print(f"Horário atual: {message}")
            except json.JSONDecodeError:
                #  TODO: transform in a switch with a type time to handle this print. Use jsondecodeerror only for error handler
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

    if user_id == "":
        user_id = "default"
    if connection == "":
        connection = "ws://localhost:2222"
    # TODO: you need to receive host in a variable instead of a hardcoded value, so docker container can set it
    async with websockets.connect(connection) as websocket:
        print("Conectado ao servidor.")
        await authenticate(websocket, user_id)

        await asyncio.gather(
            receive_messages(websocket),
            send_input_from_usr(websocket)
        )


if __name__ == "__main__":
    asyncio.run(main())
