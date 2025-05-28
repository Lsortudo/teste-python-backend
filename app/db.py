import os
from datetime import datetime

import asyncpg

class DB:
    def __init__(self, db_password, db_name, db_user, db_host):
        self.host = db_host
        self.password = db_password
        self.name = db_name
        self.user = db_user
        self.pool = None

    async def connect_db(self):
        print(f"postgres://{self.user}:{self.password}@{self.host}/{self.name}?sslmode=disable")
        self.pool = await asyncpg.create_pool(
            dsn=f"postgres://{self.user}:{self.password}@{self.host}/{self.name}?sslmode=disable",
        )
        print("connected")

    async def create_table(self):
        async with self.pool.acquire() as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS connected_users (id INTEGER PRIMARY KEY, connected_at TIMESTAMP, connected BOOLEAN)
            """)

    async def upsert_connected_user(self, user_id):
        async with self.pool.acquire() as db:
            await db.execute(
                """INSERT INTO connected_users (id, connected_at, connected)
                   values ($1, $2, TRUE) ON CONFLICT (id) DO
                   UPDATE
                   SET connected = TRUE, connected_at = EXCLUDED.connected_at""", user_id, datetime.now()
            )

    async def disconnect_user(self, user_id):
        async with self.pool.acquire() as db:
            await db.execute("""
                             UPDATE connected_users
                             SET connected = FALSE
                             WHERE id = $1
                             """, user_id)

    async def close_db(self):
        await self.pool.close()