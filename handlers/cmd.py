import re

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from sqlalchemy import select

from keyboards.for_cmd import start
from models import Task, User, async_session


router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    user_id = message.from_user.id

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

    await message.answer('Выберите действие', reply_markup=start())


@router.message(F.text.lower() == 'показать список задач')
async def task_list_choice(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text='Актуальные задачи',
        callback_data='show_current_tasks'
    ))
    builder.row(types.InlineKeyboardButton(
        text='Выполненые задачи',
        callback_data='show_completed_tasks'
    ))
    await message.answer('Выберите задачи: ', reply_markup=builder.as_markup())


@router.callback_query(F.data == 'show_current_tasks')
async def show_current_task(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            result = await session.execute(select(Task).where(
                Task.user_id == user.telegram_id
                )
            )
            tasks = result.scalars().all()
            if tasks:
                for task in tasks:
                    if not task.completed:
                        await callback.message.answer(
                            f'Задача {task.id}: {task}'
                        )
                        await callback.answer('')
            else:
                await callback.answer(
                    text='У вас нету добавленых задач',
                    show_alert=True)
        await session.commit()


@router.callback_query(F.data == 'show_completed_tasks')
async def show_completed_tasks(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id

    async with async_session() as session:
        async with session.begin():
            user = await session.get(User, telegram_id)
            result = await session.execute(select(Task).where(
                Task.user_id == user.telegram_id
                )
            )
            tasks = result.scalars().all()
            if tasks:
                for task in tasks:
                    if task.completed:
                        await callback.message.answer(
                            f'Задача {task.id}: {task}'
                        )
                        await callback.answer('')
                    else:
                        await callback.answer(
                            text='У вас нет выполненых задач',
                            show_alert=True)
        await session.commit()


class Form(StatesGroup):
    task_one_step = State()
    task_two_step = State()


@router.message(F.text.lower() == 'добавить задачу')
async def enter_task(message: Message, state: FSMContext):
    await message.answer("Введите задачу: ")
    await state.set_state(Form.task_one_step.state)


@router.message(Form.task_one_step)
async def add_task(message: Message, state: FSMContext):
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
        text='Отметить выполненой',
        callback_data=f'complite {task_id}')
        )
    builder.add(types.InlineKeyboardButton(
        text='Удалить запись',
        callback_data=f'delete {task_id}')
        )
    inline_kb = builder.as_markup()
    await state.clear()
    await message.answer(
        text=f'Задача {task_text} добавлена.',
        reply_markup=inline_kb
    )


@router.callback_query(F.data.startswith('delete'))
async def delete(callback: types.CallbackQuery):
    _, task_id = callback.data.split()
    return print(task_id)
