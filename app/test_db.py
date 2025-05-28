import asyncio
import asyncpg

async def test_connection():
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="1234",
            database="websocketdb",
            host="localhost"
        )
        print("Conectado")
        await conn.close()
    except Exception as e:
        print("N conectou, motivo > ", e)

asyncio.run(test_connection())
