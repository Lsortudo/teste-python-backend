import asyncio
import json
import os
import websockets
from datetime import datetime

from db import DB
from fibonacci import fibonacci

CONNECTIONS = set()

async def send_timer():
    try:
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            msg = json.dumps({"type": "time", "data": now})
            websockets.broadcast(CONNECTIONS, msg)
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        return

def make_handle_connection(current_db: DB):
    async def handle_connection(conn: websockets.ServerConnection):
        CONNECTIONS.add(conn)
        user_id = ""
        try:
            async for raw_message in conn:
                try:
                    message = json.loads(raw_message)
                    if message["type"] == "fibo":
                        n = int(message["data"])
                        result = fibonacci(n)
                        response = json.dumps({"type": "fibo", "input": n, "data": result})
                        await conn.send(response)
                    elif message["type"] == "auth":
                        message_user_id = int(message["data"])
                        user_id = message_user_id
                        await current_db.upsert_connected_user(user_id)
                except ValueError:
                    await conn.send(json.dumps({
                        "type": "error", "message": "mensagem inválida"
                    }))
        except websockets.ConnectionClosed:
            if user_id != "":
                await current_db.disconnect_user(user_id)
            CONNECTIONS.remove(conn)
    return handle_connection



async def main():
    ws_host = os.environ["WS_HOST"]
    ws_port = os.environ["WS_PORT"]

    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_database = os.environ["DB_DATABASE"]
    db_host = os.environ["DB_HOST"]

    current_db = DB(db_password,db_database, db_user, db_host)
    print("Current db: ", current_db)
    await current_db.connect_db()

    await current_db.create_table()

    async with websockets.serve(make_handle_connection(current_db), ws_host, int(ws_port)):
        print(f"WebSocket server started at ws://{ws_host}:{ws_port}")
        asyncio.create_task(send_timer())
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
