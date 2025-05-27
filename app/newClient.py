import asyncio
import json
import websockets

async def receive_messages(ws):
    try:
        while True:
            message = await ws.recv()
            try:
                data = json.loads(message)
                if data["type"] == "fibo":
                    print(f"\n\nFibonacci de {data['input']}: {data['result']}\n\n")
                elif data["type"] == "error":
                    print(f"Erro: {data['message']}")
            except json.JSONDecodeError:
                print(f"Horário atual: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor encerrada.")

async def send_input_from_usr(ws):
    try:
        while True:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Digite um número para calcular o Fibonacci:\n")
            await ws.send(user_input)
    except websockets.exceptions.ConnectionClosed:
        print("Conexão com o servidor encerrada.")

async def main():
    async with websockets.connect("ws://localhost:8765") as websocket:
        print("Conectado ao servidor.")
        await asyncio.gather(
            receive_messages(websocket),
            send_input_from_usr(websocket)
        )

if __name__ == "__main__":
    asyncio.run(main())
