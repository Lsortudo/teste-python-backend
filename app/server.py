import asyncio
import json
import uuid

import asyncpg
import websockets
from datetime import datetime

from fibonacci import fibonacci

CONNECTIONS = set()

db_user = "postgres"
db_password = "1234"
db_database = "websocketdb"
db_host = "localhost"

async def connect_db():
    return await asyncpg.connect(
        user=db_user,
        password=db_password,
        database=db_database,
        host=db_host
    )

async def send_timer():
    try:
        while True:
            now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            #await ws.send(now) # TODO: I think here you need the
            msg = json.dumps({"type": "time", "data": now})
            websockets.broadcast(CONNECTIONS, msg)
            await asyncio.sleep(1)
    except websockets.ConnectionClosed:
        return # remover esse try e except e testar se funciona

async def handle_connection(conn: websockets.ServerConnection):
    CONNECTIONS.add(conn)
    user_id = ""
    #session uuid
    #ip = conn.remote_address[0]
    try:
        async for raw_message in conn:
            #print(f"Recebido: {message}")
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
                    db = await connect_db()
                    await db.execute(
                         """INSERT INTO connected_users (id, connected_at, connected)
                         values ($1, $2, TRUE) ON CONFLICT (id) DO UPDATE SET connected = TRUE, connected_at = EXCLUDED.connected_at""", user_id, datetime.now()
                    )
                    await db.close()
                    # TODO: handle authentication via websocket to identify user and update his status on db.
                    #message_user_id = int(message["data"])
                    # TODO: upsert on database user: id and connected: true
                    #user_id = message_user_id
            except ValueError:
                await conn.send(json.dumps({
                    "type": "error", "message": "mensagem inválida"
                }))
    except websockets.ConnectionClosed:
        if user_id != "":
            db = await connect_db()
            await db.execute("""
            UPDATE connected_users
            SET connected = FALSE
            WHERE id = $1
            """, user_id)
            await db.close()
        CONNECTIONS.remove(conn)
                     # TODO: update to connected: false user_id



async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        print("WebSocket server started on ws://localhost:8765")
        asyncio.create_task(send_timer())
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
