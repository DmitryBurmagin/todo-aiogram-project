import asyncio
import logging

from config_reader import config
from sqlalchemy import select
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from models import Task, User, async_session
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.bot_token.get_secret_value())

dp = Dispatcher()


@dp.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    kb = [
        [
            types.KeyboardButton(text='Добавить задачу'),
            types.KeyboardButton(text='Показать список задач'),
            types.KeyboardButton(text='Удалить задачу')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Добавим задачу?'
    )

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, user_id)
            if user is None:
                user = User(
                    telegram_id=user_id,
                )
                session.add(user)
                await session.flush()
        await session.commit()

    await message.answer('Выберите действие', reply_markup=keyboard)


@dp.message(F.text.lower() == 'показать список задач')
async def task_list(message: types.Message):
    telegram_id = message.from_user.id

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            result = await session.execute(select(Task).where(
                Task.user_id == user.telegram_id
                )
            )
            tasks = result.scalars().all()
            if tasks is not None:
                for task in tasks:
                    await message.answer(f'Задача {task.id}: {task}')
            else:
                await message.answer('У вас нету добавленых задач')
        await session.commit()


@dp.message(F.text.lower() == 'добавить задачу')
async def add_task(message: types.Message):
    task_text = message.text.strip()
    telegram_id = message.from_user.id

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            task = Task(todo=task_text, user_id=user.telegram_id)
            session.add(task)
            await session.flush()
            task_id = task.id
        await session.commit()

    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text='Удалить запись',
        callback_data=f'delete {task_id}'
    ))
    inline_kb = builder.as_markup()
    await bot.send_message(
        chat_id=message.chat.id,
        text=f'Задача {task_text} добавлена.',
        reply_markup=inline_kb
    )


@dp.callback_query(F.data.startswith('delete'))
async def process_callback_button1(callback_query: types.CallbackQuery):
    telegram_id = callback_query.from_user.id
    task_text = callback_query.data.split('delete', 1)[1]
    task_id = int(task_text)

    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(Task).where(
                Task.id == task_id
                )
            )
            task = result.scalars().first()
            if task and task.user_id == telegram_id:
                await session.delete(task)
        await session.commit()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f'Запись номер {task_id} удалена'
    )


async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())
