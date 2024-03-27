from sqlalchemy import insert, select, delete

from .db import Task, User, async_session


async def task_list(telegram_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            result = await session.execute(select(Task).where(
                Task.user_id == user.telegram_id
                )
            )
            await session.commit()
            return result.scalars().all()


async def create_task(task_text: str, telegram_id: int):
    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            stmt = insert(Task).values(
                todo=task_text,
                user_id=user.telegram_id
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.inserted_primary_key[0]


async def delete_task(task_id: int):
    async with async_session() as session:
        async with session.begin():
            stmt = delete(Task).where(Task.id == task_id)
            await session.execute(stmt)
            await session.commit()
