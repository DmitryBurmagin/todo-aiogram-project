from sqlalchemy import insert, select, delete
from contextlib import asynccontextmanager

from .db import Task, User, async_session


class SessionManager:
    def __init__(self, session):
        self.session = session

    @asynccontextmanager
    async def get_session(self):
        async with self.session() as session:
            async with session.begin():
                yield session


session_manager = SessionManager(async_session)


async def task_list(telegram_id: int):
    async with session_manager.get_session() as session:
        user = await session.get(User, telegram_id)
        result = await session.execute(select(Task).where(
            Task.user_id == user.telegram_id
            )
        )
        return result.scalars().all()


async def create_task(task_text: str, telegram_id: int):
    async with session_manager.get_session() as session:
        user = await session.get(User, telegram_id)
        stmt = insert(Task).values(
            todo=task_text,
            user_id=user.telegram_id
        )
        result = await session.execute(stmt)
        return result.inserted_primary_key[0]


async def delete_task(task_id: int):
    async with session_manager.get_session() as session:
        stmt = delete(Task).where(Task.id == task_id)
        await session.execute(stmt)
